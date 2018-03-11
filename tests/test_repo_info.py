# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from gitflow_easyrelease import RepoInfo


class RepoInfoTestCase(TestCase):

    def setUp(self):
        self.construct_repo()
        self.addCleanup(self.wipe_repo)

    def wipe_repo(self):
        del self.repo

    def construct_repo(self):
        get_release_prefix_patcher = patch.object(
            RepoInfo,
            'get_release_prefix'
        )
        self.mock_get_release_prefix = get_release_prefix_patcher.start()
        get_active_branch_patcher = patch.object(
            RepoInfo,
            'get_active_branch'
        )
        self.mock_get_active_branch = get_active_branch_patcher.start()
        self.repo = RepoInfo()
        get_release_prefix_patcher.stop()
        get_active_branch_patcher.stop()


class ConstructorUnitTests(RepoInfoTestCase):

    def test_calls(self):
        self.mock_get_release_prefix.assert_called_once_with()
        self.mock_get_active_branch.assert_called_once_with()


class IsReleaseBranchUnitTests(RepoInfoTestCase):
    """"""


class TidyBranchUnitTests(RepoInfoTestCase):
    """"""


class ToSemverArgsUnitTests(RepoInfoTestCase):
    """"""


class EnsureGitFlowUnitTests(RepoInfoTestCase):
    """"""


class GetReleasePrefixUnitTests(RepoInfoTestCase):
    """"""


class GetActiveBranchUnitTests(RepoInfoTestCase):
    """"""


class GetBranchesUnitTests(RepoInfoTestCase):
    """"""


class GetTagsUnitTests(RepoInfoTestCase):
    """"""


class GetSemverTagsUnitTests(RepoInfoTestCase):
    """"""
