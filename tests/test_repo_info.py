# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from gitflow_easyrelease import RepoInfo


class RepoInfoTestCase(TestCase):
    PREFIX = 'release/'
    FEATURE_BRANCH = 'feature/qqq'
    RELEASE_BRANCH = 'release/zzz'

    def setUp(self):
        self.construct_repo()
        self.addCleanup(self.wipe_repo)

    def wipe_repo(self):
        del self.repo_info

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
        self.repo_info = RepoInfo()
        get_release_prefix_patcher.stop()
        get_active_branch_patcher.stop()


class ConstructorUnitTests(RepoInfoTestCase):

    def test_calls(self):
        self.mock_get_release_prefix.assert_called_once_with()
        self.mock_get_active_branch.assert_called_once_with()


class IsReleaseBranchUnitTests(RepoInfoTestCase):

    def setUp(self):
        RepoInfoTestCase.setUp(self)
        self.repo_info.prefix = self.PREFIX

    def test_doesnt_start_with(self):
        self.repo_info.branch = self.FEATURE_BRANCH
        self.assertFalse(self.repo_info.is_release_branch())


class TidyBranchUnitTests(RepoInfoTestCase):

    def setUp(self):
        RepoInfoTestCase.setUp(self)
        self.repo_info.prefix = self.PREFIX

    def test_tidy_feature_branch(self):
        self.repo_info.branch = self.FEATURE_BRANCH
        self.assertEqual(
            self.repo_info.tidy_branch(),
            self.FEATURE_BRANCH
        )

    def test_tidy_release_branch(self):
        self.repo_info.branch = self.RELEASE_BRANCH
        self.assertEqual(
            self.repo_info.tidy_branch(),
            'zzz'
        )


class ToSemverArgsUnitTests(RepoInfoTestCase):
    SEMVER = '1.2.3'

    @patch.object(RepoInfo, 'tidy_branch', return_value=SEMVER)
    @patch.object(RepoInfo, 'is_release_branch', return_value=False)
    def test_feature_branch(self, mock_release, mock_tidy):
        mock_tidy.assert_not_called()
        mock_release.assert_not_called()
        self.assertIsNone(self.repo_info.to_semver_args())
        mock_tidy.assert_not_called()
        mock_release.assert_called_once_with()

    @patch.object(RepoInfo, 'tidy_branch', return_value=SEMVER)
    @patch.object(RepoInfo, 'is_release_branch', return_value=True)
    def test_release_branch(self, mock_release, mock_tidy):
        mock_tidy.assert_not_called()
        mock_release.assert_not_called()
        self.assertEqual(
            ['1', '2', '3'],
            self.repo_info.to_semver_args()
        )
        mock_tidy.assert_called_once_with()
        mock_release.assert_called_once_with()


class EnsureGitFlowUnitTests(RepoInfoTestCase):

    @staticmethod
    @patch('gitflow_easyrelease.repo_info.check_output')
    def test_call(mock_check):
        mock_check.assert_not_called()
        RepoInfo.ensure_git_flow()
        mock_check.assert_called_once_with(['which', 'git-flow'])


class GetReleasePrefixUnitTests(RepoInfoTestCase):

    @staticmethod
    @patch('gitflow_easyrelease.repo_info.check_output')
    def test_call(mock_check):
        mock_check.assert_not_called()
        RepoInfo.get_release_prefix()
        mock_check.assert_called_once_with([
            'git',
            'config',
            'gitflow.prefix.release'
        ])


class GetActiveBranchUnitTests(RepoInfoTestCase):

    @staticmethod
    @patch('gitflow_easyrelease.repo_info.check_output')
    def test_call(mock_check):
        mock_check.assert_not_called()
        RepoInfo.get_active_branch()
        mock_check.assert_called_once_with([
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD'
        ])


class GetBranchesUnitTests(RepoInfoTestCase):

    @staticmethod
    @patch('gitflow_easyrelease.repo_info.check_output')
    def test_call(mock_check):
        mock_check.assert_not_called()
        RepoInfo.get_branches()
        mock_check.assert_called_once_with([
            'git',
            'for-each-ref',
            '--format',
            '%(refname:short)',
            'refs/heads/',
            'refs/remotes/'
        ])


class GetTagsUnitTests(RepoInfoTestCase):

    @staticmethod
    @patch('gitflow_easyrelease.repo_info.check_output')
    def test_call(mock_check):
        mock_check.assert_not_called()
        RepoInfo.get_tags()
        mock_check.assert_called_once_with(['git', 'tag'])


class GetSemverTagsUnitTests(RepoInfoTestCase):
    """"""
