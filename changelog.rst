=========
Changelog
=========

Changes in version 1.3.0
------------------------
- Added support for Python 3.11 and 3.12.  Dropped support for Python versions
  less than 3.7.
- Dropped support for PyMongo versions less than 4.0.

Changes in version 1.2.0
------------------------
- Added ability to configure explain command options using constructor
  keyword parameters ``verbosity`` and ``comment``.
- Added support for PyMongo 4.0
- Added support for Python 3.9 and 3.10

Changes in version 1.1.1
------------------------
- ``ExplainCollection`` now importable from top level like so: ``from pymongoexplain import ExplainCollection``
- Added aliases so that now both ``ExplainCollection`` and ``ExplainableCollection`` are importable

Changes in version 1.1.0
------------------------
- Added better commandline argument parsing to the CLI tool
- Various fixes to the documentation

Changes in version 1.0.0
------------------------
- Initial ``ExplainCollection`` API
