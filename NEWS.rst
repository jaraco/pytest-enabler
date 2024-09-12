v3.3.0
======

Features
--------

- Get Traversable from importlib.abc or importlib_resources.abc for better compatibility with Python 3.14.


v3.2.0
======

Features
--------

- Complete annotations and add ``py.typed`` marker -- by :user:`Avasam` (#18)


v3.1.1
======

Bugfixes
--------

- Ensure importlib_resources is included in the dependencies removed for coverage concerns.


v3.1.0
======

Features
--------

- Rely on stdlib for importlib.resources where compatible.


v3.0.0
======

Deprecations and Removals
-------------------------

- Renamed the plugin from 'plugin-enabled options' to 'enabler'. (#12)
- Ruff formatter is now enabled by default. (#13)


v2.3.1
======

Bugfixes
--------

- Fix default config for ignore-flaky.


v2.3.0
======

Features
--------

- Added support for pytest-ignore-flaky.


Bugfixes
--------

- If pytest-cov is explicitly enabled, bypass special handling. (#8)


v2.2.0
======

Features
--------

- Enabler plugin now includes a default config, enabling the known supported plugins. It's no longer necessary for each project to supply the config to enable plugins.
- Require Python 3.8 or later.


v2.1.1
======

Packaging refresh.

v2.1.0
======

Fixed EncodingWarning when PEP 597 warn_default_encoding is enabled.

v2.0.0
======

#4: Remove compatibility shim. ``[pytest.enabler]`` is no longer
supported.

v1.3.1
======

Packaging refresh.

v1.3.0
======

#4: pytest-enabler now uses ``[tool.pytest-enabler]`` for configuration
in accordance with :pep:`518#tool-table` (``[pytest.enabler]`` is deprecated).

v1.2.1
======

Packaging refresh.

v1.2.0
======

Simplified implementation.

v1.1.0
======

#2: Package now properly recognizes the ``pytest_cov`` plugin
as ``cov`` (and same for others).

v1.0.1
======

#1: Fixed race condition between pytest-cov and pytest-xdist.

v1.0.0
======

Initial implementation, based on
`jaraco.test 4.0.1 <https://pypi.org/project/jaraco.test>_`.
