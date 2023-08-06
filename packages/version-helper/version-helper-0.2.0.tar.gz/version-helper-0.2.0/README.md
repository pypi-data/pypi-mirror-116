# Version helper

`version-helper` is a package for a better version management in python projects.

_This package is still under development. Code may change frequently._

![PyPI](https://img.shields.io/pypi/v/version-helper)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/version-helper)
[![codecov](https://codecov.io/gh/dl6nm/version-helper/branch/main/graph/badge.svg?token=WNOMQ28E5J)](https://codecov.io/gh/dl6nm/version-helper)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dl6nm/version-helper/Codecov%20Workflow)
![Lines of code](https://img.shields.io/tokei/lines/github/dl6nm/version-helper)
![GitHub](https://img.shields.io/github/license/dl6nm/version-helper)

    from version_helper import Version

    # Parse output from `git describe --tag` and 
    # return a semantic versioning compatible `Version` object
    v = Version.get_from_git_describe()

    # Output core version string including major, minor and patch
    print(v.core)

    # Output full Semantic Version string including core, prerelease and build metadata
    print(v.full)

## Table of contents

- [Version helper](#version-helper)
  - [Table of contents](#table-of-contents)
  - [Installing `version-helper`](#installing-version-helper)
  - [Usage](#usage)
    - [Reading version from a file](#reading-version-from-a-file)
    - [Writing version to a file](#writing-version-to-a-file)
  - [Changelog](#changelog)
  - [References](#references)

## Installing `version-helper`

    pip install version-helper

Code example see at the top of this page.

## Usage

### Reading version from a file

    import pathlib
    from version_helper import Version
    
    version = Version.read_from_file(
        file=pathlib.Path('/path/to/my/version_file.txt'),
        variable_name='APP_VERSION',
        separator='=',
    )
    print(version)

### Writing version to a file

    import pathlib
    from version_helper import Version
    
    version = Version(1, 2, 3)
    version.write_to_file(
        file=pathlib.Path('/path/to/my/version_file.txt'),
        variable_name='APP_VERSION',
        separator='=',
    )

## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md).

## References

- [git-describe](https://git-scm.com/docs/git-describe)
- [Poetry](https://python-poetry.org/)
- [Semantic Versioning](https://semver.org/)
