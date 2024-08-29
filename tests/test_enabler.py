from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

import pytest_enabler as enabler


@pytest.fixture
def pyproject(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path / 'pyproject.toml'


def test_pytest_addoption_default() -> None:
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args: list[str] = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == ['--black']


def test_pytest_addoption_override(pyproject: Path) -> None:
    pyproject.write_text(
        '[tool.pytest-enabler.black]\naddopts="--black2"\n',
        encoding='utf-8',
    )
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args: list[str] = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == ['--black2']


def test_pytest_addoption_disable(pyproject: Path) -> None:
    pyproject.write_text(
        '[tool.pytest-enabler.black]\n#addopts="--black"\n',
        encoding='utf-8',
    )
    config = mock.MagicMock()
    config.pluginmanager.has_plugin = lambda name: name == 'black'
    args: list[str] = []
    enabler.pytest_load_initial_conftests(config, None, args)
    assert args == []


def test_remove_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Invoke _remove_deps to push coverage.
    """
    monkeypatch.setattr(sys, 'modules', dict(sys.modules))
    enabler._remove_deps()


def test_coverage_explicit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    test = tmp_path.joinpath('test_x.py')
    test.write_text('def test_x():\n    pass\n', encoding='utf-8')
    subprocess.check_call([sys.executable, '-m', 'pytest', '--cov'])
