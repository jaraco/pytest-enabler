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
