"""This file provides the Git class"""

from __future__ import print_function

from subprocess import check_output


class Git:
    """This utility class provides information about the underlying repo"""
    # TODO: rename

    def __init__(self):
        self.prefix = Git.get_release_prefix()
        self.branch = Git.get_active_branch()

    def is_release_branch(self):
        return self.branch.startswith(self.prefix)

    @staticmethod
    def ensure_git_flow():
        check_output(['which', 'git-flow'])

    @staticmethod
    def get_release_prefix():
        return check_output([
            'git',
            'config',
            'gitflow.prefix.release'
        ]).strip()

    @staticmethod
    def get_active_branch():
        return check_output([
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD'
        ]).strip()

    @staticmethod
    def get_branches():
        return check_output([
            'git',
            'for-each-ref',
            '--format',
            '%(refname:short)',
            'refs/heads/',
            'refs/remotes/'
        ]).strip().split('\n')
