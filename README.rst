.. image:: https://img.shields.io/pypi/v/pytest-enabler.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/pytest-enabler.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/pytest-enabler

.. image:: https://github.com/jaraco/pytest-enabler/workflows/tests/badge.svg
   :target: https://github.com/jaraco/pytest-enabler/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

The 'enabler' plugin allows configuration of plugins if present, but omits the settings if the plugin is not present. For example, to configure black to be enabled if the plugin is present, but not when it is not, add the following to your pyproject.toml::

    [pytest.enabler.black]
    addopts = "--black"
