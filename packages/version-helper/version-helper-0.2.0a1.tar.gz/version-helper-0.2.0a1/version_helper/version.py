import pathlib
import re

from version_helper import Git

SEMVER_PATTERN = r'^(?P<major>0|(?:[1-9]\d*))(?:\.(?P<minor>0|(?:[1-9]\d*))(?:\.(?P<patch>0|(?:[1-9]\d*)))(?:\-(?P<prerelease>[\w\d\.-]+))?(?:\+(?P<build>[\w\d\.-]+))?)?$'
GIT_DESCRIBE_PATTERN = r'^(?P<major>0|(?:[1-9]\d*))(?:\.(?P<minor>0|(?:[1-9]\d*)))(?:\.(?P<patch>0|(?:[1-9]\d*)))(?:\-(?P<prerelease>(?:[\w\d\-]+\.?)+)(?=\-(?:\d+\-[\w\d]{8}(?:\-[\d\w\-]+)?)$))?(?:\-(?P<build>\d+\-[\w\d]{8}(?:\-[\d\w\-]+)?))?$'


class Version:
    """Semantic Versioning compatible class for parsing and emitting SemVer strings into a `Version` object

    More details on Semantic Versioning can be found at https://semver.org/
    """

    def __init__(self, major: int, minor: int, patch: int,
                 prerelease: str = None, build: str = None):
        """Create a `Version` object with the given attributes

        :param major: MAJOR version when you make incompatible API changes
        :param minor: MINOR version when you add functionality in a backwards compatible manner
        :param patch: PATCH version when you make backwards compatible bug fixes
        :param prerelease: Pre-release version string like `alpha.0` or `beta.3`
        :param build: Build metadata
        """
        self.major: int = major
        self.minor: int = minor
        self.patch: int = patch
        self.prerelease: str = prerelease
        self.build: str = build

    def __repr__(self):
        return self.full

    def __str__(self):
        return self.full

    @staticmethod
    def parse(string: str, is_from_git_describe: bool = False) -> 'Version':
        """Parse a version string into it's individual Semantic Versioning parts

        :param string: A Semantic Versioning string
        :param is_from_git_describe: Wether or not the version string is from `git describe`
        :return: A `Version` class object
        """
        pattern = SEMVER_PATTERN
        if is_from_git_describe:
            pattern = GIT_DESCRIBE_PATTERN

        match = None
        if string:
            match = re.fullmatch(pattern, string.strip())

        if match:
            match_dict = match.groupdict()

            return Version(
                major=int(match_dict.get('major')),
                minor=int(match_dict.get('minor')),
                patch=int(match_dict.get('patch')),
                prerelease=match_dict.get('prerelease'),
                build=match_dict.get('build'),
            )
        else:
            raise ValueError('`version_string` is not valid to Semantic Versioning Specification')

    @classmethod
    def get_from_git_describe(cls, dirty=False) -> 'Version':
        """Get a semantic version from git describe

        :param dirty: Append '-dirty' to the build context, if the working tree has local modifications
        :return: A `Version` class object
        """
        description = Git.describe(dirty=dirty)
        return cls.parse(description, True)

    def set(self, major: int, minor: int, patch: int,
            prerelease: str = None, build: str = None):
        """Set `Version` attributes

        :param major: MAJOR version when you make incompatible API changes
        :param minor: MINOR version when you add functionality in a backwards compatible manner
        :param patch: PATCH version when you make backwards compatible bug fixes
        :param prerelease: Pre-release version string like `alpha.0` or `beta.3`
        :param build: Build metadata
        """
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.build = build

    @property
    def core(self) -> str:
        """Core version string including major, minor and patch

        :return: Core version string
        """
        return f'{self.major}.{self.minor}.{self.patch}'

    @property
    def full(self) -> str:
        """Full Semantic Version string including prerelease and build metadata

        :return: Full version string with all it's Semantic Versioning parts
        """
        semver = f'{self.major}.{self.minor}.{self.patch}'
        if self.prerelease:
            semver += f'-{self.prerelease}'
        if self.build:
            semver += f'+{self.build}'
        return semver

    @staticmethod
    def read_from_file(file: pathlib.Path, variable_name: str = '__version__', separator: str = '=') -> 'Version':
        if not separator and variable_name:
            raise ValueError('None value for separator. Could not parse file.')
        if not variable_name and separator:
            raise ValueError('None value for variable_name. Could not parse file.')

        version_string = None

        if file.suffix == '.py':
            if separator != '=':
                raise ValueError('Only "=" is allowed as separator for .py files. Could not parse file.')

            # load python file as module
            from importlib.util import spec_from_loader, module_from_spec
            from importlib.machinery import SourceFileLoader

            spec = spec_from_loader("version_file", SourceFileLoader("version_file", str(file.absolute())))
            version_file = module_from_spec(spec)
            spec.loader.exec_module(version_file)

            # get version string
            version_string = eval(f"version_file.{variable_name}")
        else:
            with open(file, 'r') as f:
                line = f.readline().strip()
                while line:
                    if variable_name and separator:
                        if line.startswith(variable_name):
                            version_string = line.split(separator, 1)[1].strip()
                            break
                    else:
                        version_string = line.strip()
                        break
                    line = f.readline().strip()

        return Version.parse(version_string)

