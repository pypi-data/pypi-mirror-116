# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['version_helper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'version-helper',
    'version': '0.2.0a1',
    'description': 'Helpers for a better version management in python projects',
    'long_description': '# Version Helper\n\n`version-helper` is a package for a better version management in python projects.\n\n_This package is still under development. Code may change frequently._\n\n![PyPI](https://img.shields.io/pypi/v/version-helper)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/version-helper)\n[![codecov](https://codecov.io/gh/dl6nm/version-helper/branch/main/graph/badge.svg?token=WNOMQ28E5J)](https://codecov.io/gh/dl6nm/version-helper)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dl6nm/version-helper/Codecov%20Workflow)\n![Lines of code](https://img.shields.io/tokei/lines/github/dl6nm/version-helper)\n![GitHub](https://img.shields.io/github/license/dl6nm/version-helper)\n\n    from version_helper import Version\n\n    # Parse output from `git describe --tag` and \n    # return a semantic versioning compatible `Version` object\n    v = Version.get_from_git_describe()\n\n    # Output core version string including major, minor and patch\n    print(v.core)\n\n    # Output full Semantic Version string including core, prerelease and build metadata\n    print(v.full)\n\n## Table of Contents\n\n- [Version Helper](#version-helper)\n  - [Table of Contents](#table-of-contents)\n  - [Installing `version-helper`](#installing-version-helper)\n  - [Publish](#publish)\n  - [Changelog](#changelog)\n  - [References](#references)\n\n## Installing `version-helper`\n\n    pip install version-helper\n\nCode example see at the top of this page.\n\n## Publish\n\n    poetry publish --build [-r testpypi]\n\n## Changelog\n\nAll notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md).\n\n## References\n\n- [git-describe](https://git-scm.com/docs/git-describe)\n- [Poetry](https://python-poetry.org/)\n- [Semantic Versioning](https://semver.org/)\n',
    'author': 'DL6NM',
    'author_email': 'mail@dl6nm.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dl6nm/version-helper',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
