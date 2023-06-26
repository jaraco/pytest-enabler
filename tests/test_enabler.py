import sys
from unittest import mock

import pytest

import pytest_enabler as enabler


@pytest.fixture
def pyproject(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    return tmp_path / 'pyproject.toml'


def test_pytest_addoption_default():
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == ['--black']


def test_pytest_addoption_override(pyproject):
    pyproject.write_text('[tool.pytest-enabler.black]\naddopts="--black2"\n')
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == ['--black2']


def test_pytest_addoption_disable(pyproject):
    pyproject.write_text('[tool.pytest-enabler.black]\n#addopts="--black"\n')
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == []


def test_remove_deps(monkeypatch):
    """
    Invoke _remove_deps to push coverage.
    """
    monkeypatch.setattr(sys, 'modules', dict(sys.modules))
    enabler._remove_deps()
