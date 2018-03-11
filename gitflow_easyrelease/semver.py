"""This file provides the SemVer class"""

from __future__ import print_function

from re import compile as re_compile, match
from subprocess import check_output


class SemVer(object):
    """This class encapsulates semantic versioning logic."""

    PATCH_KEYS = ['p', 'patch', '~']
    MINOR_KEYS = ['m', 'minor', '^']
    MAJOR_KEYS = ['M', 'major']
    ALL_KEYS = PATCH_KEYS + MINOR_KEYS + MAJOR_KEYS

    SEMVER_PATTERN = re_compile(r'\s*v?\d+\.\d+\.\d+\s*')

    def __init__(self, major=0, minor=0, patch=0):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def compare(self, version=None):
        if version:
            for component in ['major', 'minor', 'patch']:
                comparison = SemVer.compare_component(
                    getattr(self, component),
                    getattr(version, component)
                )
                if 0 != comparison:
                    return comparison
            return 0
        return -1

    def greater(self, version=None):
        return -1 == self.compare(version)

    def lesser(self, version=None):
        return 1 == self.compare(version)

    def equal(self, version=None):
        return 0 == self.compare(version)

    def bump(self, component=None):
        if component in SemVer.ALL_KEYS:
            if component in SemVer.PATCH_KEYS:
                self.patch = self.patch + 1
            else:
                self.patch = 0
                if component in SemVer.MINOR_KEYS:
                    self.minor = self.minor + 1
                else:
                    self.minor = 0
                    self.major = self.major + 1
        return self

    def __repr__(self):
        return "%d.%d.%d" % (self.major, self.minor, self.patch)

    @staticmethod
    def compare_component(first, second):
        if first < second:
            return 1
        elif first > second:
            return -1
        return 0

    @staticmethod
    def from_version(version):
        return SemVer(*version.replace('v', '').split('.'))

    @staticmethod
    def is_semver(version):
        return not match(SemVer.SEMVER_PATTERN, version) is None

    @staticmethod
    def is_component(version):
        return version in SemVer.ALL_KEYS

    @staticmethod
    def get_active_branch():
        current = check_output([
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD'
        ]).strip()
        if current.startswith('release'):
            return SemVer(*current.replace('release/', '').split('.'))
        return None

    @staticmethod
    def get_current_version():
        active = SemVer.get_active_branch()
        if active:
            return active
        versions = [
            SemVer.from_version(version)
            for version in check_output(['git', 'tag']).strip().split('\n')
            if SemVer.is_semver(version)
        ]
        if versions:
            max_version = versions.pop()
            for version in versions:
                if version.greater(max_version):
                    max_version = version
            return max_version
        return SemVer()

    @staticmethod
    def process_version(version=None):
        if version:
            if SemVer.is_semver(version):
                return SemVer.from_version(version)
            elif SemVer.is_component(version):
                return SemVer.get_current_version().bump(version)
            return version
        return SemVer.get_active_branch()
