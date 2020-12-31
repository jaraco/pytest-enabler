import sys
import textwrap
import pathlib
from unittest import mock

import pytest

import pytest_enabler as enabler


@pytest.fixture
def tmpdir_cur(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


def test_pytest_addoption(tmpdir_cur):
    pathlib.Path('pyproject.toml').write_text(
        textwrap.dedent(
            """
            [pytest.enabler.black]
            addopts = "--black"
            """
        )
    )
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == ['--black']


def test_remove_deps(monkeypatch):
    """
    Invoke _remove_deps to push coverage.
    """
    monkeypatch.setattr(sys, 'modules', dict(sys.modules))
    enabler._remove_deps()
