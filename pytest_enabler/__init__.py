import contextlib
import pathlib
import shlex
import sys

import importlib_resources as resources

import toml
from jaraco.context import suppress
from jaraco.functools import apply


def none_as_empty(ob):
    """
    >>> none_as_empty({})
    {}
    >>> none_as_empty(None)
    {}
    >>> none_as_empty({'a': 1})
    {'a': 1}
    """
    return ob or {}


def read_plugins_stream(stream):
    defn = toml.load(stream)
    return defn["tool"]["pytest-enabler"]


@apply(none_as_empty)
@suppress(Exception)
def read_plugins(path):
    with path.open(encoding='utf-8') as stream:
        return read_plugins_stream(stream)


def pytest_load_initial_conftests(early_config, parser, args):
    plugins = {
        **read_plugins(resources.files().joinpath('default.toml')),
        **read_plugins(pathlib.Path('pyproject.toml')),
    }

    def _has_plugin(name):
        pm = early_config.pluginmanager
        return pm.has_plugin(name) or pm.has_plugin('pytest_' + name)

    enabled = {key: plugins[key] for key in plugins if _has_plugin(key)}
    for plugin in enabled.values():
        args.extend(shlex.split(plugin.get('addopts', "")))
    _pytest_cov_check(enabled, early_config, parser, args)


def _remove_deps():
    """
    Coverage will not detect function definitions as being covered
    if the functions are defined before coverage is invoked. As
    a result, when testing any of the dependencies above, their
    functions will appear not to be covered. To avoid this behavior,
    unload the modules above so they may be tested for coverage
    on import as well.
    """
    del sys.modules['jaraco.functools']
    del sys.modules['jaraco.context']
    del sys.modules['toml']
    del sys.modules['pytest_enabler']


def _pytest_cov_check(plugins, early_config, parser, args):  # pragma: nocover
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
