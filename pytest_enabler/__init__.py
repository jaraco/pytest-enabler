from __future__ import annotations

import contextlib
import os
import pathlib
import re
import shlex
import sys
from collections.abc import Container, MutableSequence, Sequence
from typing import TYPE_CHECKING, TypeVar, cast, overload

import toml
from jaraco.context import suppress
from jaraco.functools import apply
from pytest import Config, Parser

if sys.version_info >= (3, 12):
    from importlib import resources
    from importlib.resources.abc import Traversable
else:
    import importlib_resources as resources
    from importlib_resources.abc import Traversable

if TYPE_CHECKING:
    from _typeshed import SupportsRead
    from typing_extensions import Never


_T = TypeVar("_T")

consume = tuple  # type: ignore[type-arg] # Generic doesn't matter; keep it callable
"""
Consume an iterable
"""


@overload
def none_as_empty(ob: None) -> dict[Never, Never]: ...
@overload
def none_as_empty(ob: _T) -> _T: ...
def none_as_empty(ob: _T | None) -> _T | dict[Never, Never]:
    """
    >>> none_as_empty({})
    {}
    >>> none_as_empty(None)
    {}
    >>> none_as_empty({'a': 1})
    {'a': 1}
    """
    return ob or {}


def read_plugins_stream(
    stream: str | bytes | pathlib.PurePath | SupportsRead[str],
) -> dict[str, dict[str, str]]:
    defn = toml.load(stream)
    return defn["tool"]["pytest-enabler"]  # type: ignore[no-any-return]


@apply(none_as_empty)
@suppress(Exception)
def read_plugins(path: Traversable) -> dict[str, dict[str, str]]:
    with path.open(encoding='utf-8') as stream:  # type: ignore[no-untyped-call, unused-ignore]  # python/importlib_resources#137
        return read_plugins_stream(stream)


def pytest_load_initial_conftests(
    early_config: Config,
    parser: Parser | None,
    args: MutableSequence[str],
) -> None:
    plugins = {
        **read_plugins(resources.files().joinpath('default.toml')),
        **read_plugins(pathlib.Path('pyproject.toml')),
    }

    def _has_plugin(name: str) -> bool:
        pm = early_config.pluginmanager
        return pm.has_plugin(name) or pm.has_plugin('pytest_' + name)

    enabled = {key: plugins[key] for key in plugins if _has_plugin(key)}
    for plugin in enabled.values():
        args.extend(shlex.split(plugin.get('addopts', "")))
    _pytest_cov_check(
        enabled,
        early_config,
        # parser is only used when known not to be None
        # based on `enabled` and `early_config`.
        cast(Parser, parser),
        args,
    )


def _remove_deps() -> None:
    """
    Coverage will not detect function definitions as being covered
    if the functions are defined before coverage is invoked. As
    a result, when testing any of the dependencies above, their
    functions will appear not to be covered. To avoid this behavior,
    unload the modules above (and submodules) so they may be tested
    for coverage on import as well.
    """
    third_party_imports = (
        'importlib_resources',
        'jaraco.context',
        'jaraco.functools',
        'pytest_enabler',
        'toml',
    )
    pattern = re.compile('|'.join(map(re.escape, third_party_imports)))
    to_delete = tuple(filter(pattern.match, sys.modules))
    consume(map(sys.modules.__delitem__, to_delete))


def _pytest_cov_check(
    plugins: Container[str],
    early_config: Config,
    parser: Parser,
    args: Sequence[str | os.PathLike[str]],
) -> None:  # pragma: nocover
    """
    pytest_cov runs its command-line checks so early that no hooks
    can intervene. By now, the hook that installs the plugin has
    already run and failed to enable the plugin. So, parse the config
    specially and re-run the hook.
    """
    if 'cov' not in plugins:
        return

    if early_config.pluginmanager.getplugin('_cov'):
        # cov was explicitly configured (#8)
        return

    _remove_deps()
    # important: parse all known args to ensure pytest-cov can configure
    # itself based on other plugins like pytest-xdist (see #1).
    parser.parse_known_and_unknown_args(args, early_config.known_args_namespace)

    with contextlib.suppress(ImportError):
        import pytest_cov.plugin

    pytest_cov.plugin.pytest_load_initial_conftests(early_config, parser, args)
