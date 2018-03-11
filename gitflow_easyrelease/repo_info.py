"""This file provides the Git class"""

from __future__ import print_function

from subprocess import check_output

from gitflow_easyrelease import SemVer


class RepoInfo(object):
    """This utility class provides information about the underlying repo"""

    def __init__(self):
        self.prefix = RepoInfo.get_release_prefix()
        self.branch = RepoInfo.get_active_branch()

    def is_release_branch(self):
        """Checks if the active branch is a release branch"""
        return self.branch.startswith(self.prefix)

    @staticmethod
    def ensure_git_flow():
        """Ensures git flow is available"""
        check_output(['which', 'git-flow'])

    @staticmethod
    def get_release_prefix():
        """Determines the git flow release branch prefix"""
        return check_output([
            'git',
            'config',
            'gitflow.prefix.release'
        ]).strip()

    @staticmethod
    def get_active_branch():
        """Determines the active branch"""
        return check_output([
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD'
        ]).strip()

    @staticmethod
    def get_branches():
        """Gets all available branches"""
        return check_output([
            'git',
            'for-each-ref',
            '--format',
            '%(refname:short)',
            'refs/heads/',
            'refs/remotes/'
        ]).strip().split('\n')

    @staticmethod
    def get_tags():
        """Returns all defined tags"""
        return check_output(['git', 'tag']).strip().split('\n')

    @staticmethod
    def get_semver_tags():
        """Returns all semver tags"""
        return [
            version
            for version in RepoInfo.get_tags()
            if SemVer.is_semver(version)
        ]
