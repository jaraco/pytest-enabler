.. image:: https://img.shields.io/pypi/v/pytest-enabler.svg
   :target: https://pypi.org/project/pytest-enabler

.. image:: https://img.shields.io/pypi/pyversions/pytest-enabler.svg

.. image:: https://github.com/jaraco/pytest-enabler/workflows/tests/badge.svg
   :target: https://github.com/jaraco/pytest-enabler/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://readthedocs.org/projects/pytest-enabler/badge/?version=latest
   :target: https://pytest-enabler.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2023-informational
   :target: https://blog.jaraco.com/skeleton

The ``enabler`` plugin allows configuration of plugins if present, but omits the settings if the plugin is not present. For example, the following config enables black to be enabled when present::

    [tool.pytest-enabler.black]
    addopts = "--black"

Then, to temporarily disable a plugin, use pytest's built-in support for disabling a plugin::

    pytest -p no:black

``enabler`` includes a `default config <https://github.com/jaraco/pytest-enabler/blob/main/pytest_enabler/default.toml>`_.

Known to work with the following plugins:

- pytest-black
- pytest-cov
- pytest-flake8
- pytest-mypy
- pytest-ruff
- pytest-xdist
- pytest-ignore-flaky
