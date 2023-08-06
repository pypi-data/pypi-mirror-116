# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Releases]

_All releases will be published to [PyPI]._

### [0.2.2] (2021-08-19)

#### Added

- Add additional information on the "g" prefix at the front of git describes has suffix (closes #11)
- Add requirements to README.md
- Add PyPI wheel badge to README.md

#### Changed

- Change minimal python version to 3.6
- Change stdout and stderr of the subprocess to be backwards compatible with Python 3.6
- Replace apostrophes in (error) messages with normal quotes (closes #14)
- Correct spelling in docstring
- Update main workflow badge in README.md

#### Fixed

- Fix bug where an error was raised on only core version having a "-dirty" flag (closes #13)
- Fix error on asserting stderr

#### Maintenance

- Adapt PyPI classifiers and GitHub workflow
- Update GitHub action for setting up poetry
- Build and test on every push

#### Tests

- Change test to check the output of the git tools _call_process method
- Add test for a dirty repository having no commits after a tag, only changed files (#13)
- Add another test with "-dirty" flag

### [0.2.2-alpha.2] (2021-08-19)

#### Added

- Add additional information on the "g" prefix at the front of git describes has suffix (#11)
- Add wheel badge to README.md

#### Changed

- Replace apostrophes in (error) messages with normal quotes (#14)
- Correct spelling in docstring
- Update main workflow badge in README.md
- Update GitHub action for setting up poetry

#### Fixed

- Fix bug where an error was raised on only core version having a "-dirty" flag (#13)
- Fix error on asserting stderr

#### Maintenance

- Build and test on every push

#### Tests

- Add test for a dirty repository having no commits after a tag, only changed files (#13)

### [0.2.2-alpha.1] (2021-08-18)

#### Changed

- Change stdout and stderr of the subprocess to be backwards compatible with Python 3.6

### [0.2.2-alpha.0] (2021-08-18)

#### Added

- Add requirements to README.md

#### Changed

- Change minimal python version to 3.7
- Adapt PyPI classifiers
- Adapt GitHub workflow

#### Maintenance

- Refactor GitHub workflow to run only on the `main` branch

### [0.2.1] (2021-08-16)

#### Changed

- Adapt GitHub action (workflow) and test setup
- Clean-up [README.md](README.md)

#### Fixed

- Fix badge links in README.md

#### Maintenance

- Update pyproject.toml

### [0.2.0] (2021-08-13)

#### Added

- Add method `read_from_file()` to `Version` class for reading a version string from a file
- Add method `write_to_file()` to `Version` class for writing a version string to a file

#### Maintenance

- Fix problem on setting the PyPI token for publishing the package with Poetry
- Add GitHub workflows for build, release and publish this python package `version-helper`
- Add macOS and Ubuntu to the test matrix
- Add missing tests for the `Version` class dunder methods `__str__` and `__repr__`

### [0.2.0-beta.0] (2021-08-13)

- Add method `write_to_file()` to `Version` class for writing a version string to a file

### [0.2.0-alpha.1] (2021-08-12)

#### Added

- Add macOS and Ubuntu to the test matrix
- Add missing tests for the `Version` class dunder methods `__str__` and `__repr__`
- Add method `read_from_file()` to `Version` class for reading a version string from a file

#### Changed

- Add me (dl6nm) as owner explicitly for creating a new release

### [0.2.0-alpha.0] (2021-08-10)

#### Fixed

- Fix problem on setting the PyPI token for publishing the package with Poetry

### [0.1.3] (2021-08-10)

#### Added

- Add build and publish workflow job
- Include CHANGELOG.md in package

#### Fixed

- Fix problem on test coverage, avoid to cover the tests itself

### [0.1.2] (2021-08-10)

#### Fixed

- Fix error in workflow on uploading coverage report to Codecov

### [0.1.1] (2021-08-10)

#### Added

- Add GitHub workflow for running tests and getting the code coverage with [Codecov](https://app.codecov.io/gh/dl6nm/version-helper)
- Add [CHANGELOG.md](CHANGELOG.md)

### [0.1.0] (2021-08-09)

#### Added

- Add tests and fixtures for `Git` class and its methods
- Implement `Git` class with method...
  - `exec_path()` for getting the installation path of git
  - `describe()` to get a human-readable string containing the most recent tag
- Implement `Version.get_from_git_describe()` to get a `Version` object from a `git describe` call
- Add code examples to [README.md](README.md)

### [0.0.1] (2021-07-30)

#### Added

- Add tests and fixtures for `Version` class and its methods
- Implement `Version` class with method...
  - `parser()` for converting a string into a [Semantic Versioning] like `Version` object
  - `set()` for setting or changing a version explicitly
- Add [README.md](README.md)



[0.2.2]: https://github.com/dl6nm/version-helper/compare/0.2.1...0.2.2
[0.2.2-alpha.1]: https://github.com/dl6nm/version-helper/compare/0.2.2-alpha.0...0.2.2-alpha.1
[0.2.2-alpha.0]: https://github.com/dl6nm/version-helper/compare/0.2.1...0.2.2-alpha.0
[0.2.1]: https://github.com/dl6nm/version-helper/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/dl6nm/version-helper/compare/0.1.2...0.2.0
[0.2.0-beta.0]: https://github.com/dl6nm/version-helper/compare/0.2.0-alpha.1...0.2.0-beta.0
[0.2.0-alpha.1]: https://github.com/dl6nm/version-helper/compare/0.2.0-alpha.0...0.2.0-alpha.1
[0.2.0-alpha.0]: https://github.com/dl6nm/version-helper/compare/0.1.3...0.2.0-alpha.0
[0.1.3]: https://github.com/dl6nm/version-helper/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/dl6nm/version-helper/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/dl6nm/version-helper/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/dl6nm/version-helper/compare/0.0.1...0.1.0
[0.0.1]: https://github.com/dl6nm/version-helper/releases/tag/0.0.1

[releases]: https://github.com/dl6nm/version-helper/releases
[pypi]: https://pypi.org/project/version-helper/

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html
