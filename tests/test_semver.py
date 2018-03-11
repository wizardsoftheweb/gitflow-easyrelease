# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch
from pytest import mark

from gitflow_easyrelease import SemVer


class SemVerTestCase(TestCase):

    def setUp(self):
        self.construct_semver()
        self.addCleanup(self.wipe_semver)

    def wipe_semver(self):
        del self.semver

    def construct_semver(self):
        self.semver = SemVer()


class ConstructorUnitTests(SemVerTestCase):

    def test_defaults(self):
        self.assertEqual(
            self.semver.__repr__(),
            '0.0.0'
        )


class CompareUnitTests(SemVerTestCase):
    STRING_VERSION = 'v1.2.3'
    SEMVER_VERSION = SemVer(1, 2, 3)

    @patch(
        'gitflow_easyrelease.semver.SemVer.from_version',
        return_value=None
    )
    def test_semver_creation(self, mock_from):
        mock_from.assert_not_called()
        self.semver.compare(self.STRING_VERSION)
        mock_from.assert_called_once_with(self.STRING_VERSION)

    @patch(
        'gitflow_easyrelease.semver.SemVer.from_version',
        return_value=None
    )
    def test_semver_creation_skipping(self, mock_from):
        mock_from.assert_not_called()
        self.semver.compare(self.SEMVER_VERSION)
        mock_from.assert_not_called()

    @patch(
        'gitflow_easyrelease.semver.SemVer.compare_component',
        return_value=0
    )
    def test_equality_comparison(self, mock_comparison):
        mock_comparison.assert_not_called()
        self.assertEqual(
            self.semver.compare(self.SEMVER_VERSION),
            0
        )
        mock_comparison.assert_has_calls([
            call(0, 1),
            call(0, 2),
            call(0, 3)
        ])

    @patch(
        'gitflow_easyrelease.semver.SemVer.compare_component',
        return_value=1
    )
    def test_difference_comparison(self, mock_comparison):
        mock_comparison.assert_not_called()
        self.assertEqual(
            self.semver.compare(self.SEMVER_VERSION),
            1
        )
        mock_comparison.assert_called_once_with(0, 1)


class GreaterUnitTests(SemVerTestCase):
    VERSION = SemVer(1, 2, 3)

    @patch.object(
        SemVer,
        'compare',
        return_value=1
    )
    def test_lesser(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertFalse(self.semver.greater(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)

    @patch.object(
        SemVer,
        'compare',
        return_value=0
    )
    def test_equal(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertFalse(self.semver.greater(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)

    @patch.object(
        SemVer,
        'compare',
        return_value=-1
    )
    def test_greater(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertTrue(self.semver.greater(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)


class LesserUnitTests(SemVerTestCase):
    VERSION = SemVer(1, 2, 3)

    @patch.object(
        SemVer,
        'compare',
        return_value=1
    )
    def test_lesser(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertTrue(self.semver.lesser(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)

    @patch.object(
        SemVer,
        'compare',
        return_value=0
    )
    def test_equal(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertFalse(self.semver.lesser(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)

    @patch.object(
        SemVer,
        'compare',
        return_value=-1
    )
    def test_greater(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertFalse(self.semver.lesser(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)


class EqualUnitTests(SemVerTestCase):
    VERSION = SemVer(1, 2, 3)

    @patch.object(
        SemVer,
        'compare',
        return_value=1
    )
    def test_lesser(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertFalse(self.semver.equal(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)

    @patch.object(
        SemVer,
        'compare',
        return_value=0
    )
    def test_equal(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertTrue(self.semver.equal(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)

    @patch.object(
        SemVer,
        'compare',
        return_value=-1
    )
    def test_greater(self, mock_compare):
        mock_compare.assert_not_called()
        self.assertFalse(self.semver.equal(self.VERSION))
        mock_compare.assert_called_once_with(self.VERSION)


class BumpUnitTests(SemVerTestCase):
    MAJOR = 1
    MINOR = 2
    PATCH = 3

    def setUp(self):
        SemVerTestCase.setUp(self)
        self.reset_semver()

    def reset_semver(self):
        self.semver = SemVer(self.MAJOR, self.MINOR, self.PATCH)

    def test_bump_nothing(self):
        self.assertEqual(
            self.semver.__repr__(),
            '1.2.3'
        )
        self.semver.bump(' '.join(SemVer.ALL_KEYS))
        self.assertEqual(
            self.semver.__repr__(),
            '1.2.3'
        )

    def test_patch_bump(self):
        for component in SemVer.PATCH_KEYS:
            self.reset_semver()
            self.assertEqual(
                self.semver.__repr__(),
                '1.2.3'
            )
            self.semver.bump(component)
            self.assertEqual(
                self.semver.__repr__(),
                '1.2.4'
            )

    def test_minor_bump(self):
        for component in SemVer.MINOR_KEYS:
            self.reset_semver()
            self.assertEqual(
                self.semver.__repr__(),
                '1.2.3'
            )
            self.semver.bump(component)
            self.assertEqual(
                self.semver.__repr__(),
                '1.3.0'
            )

    def test_major_bump(self):
        for component in SemVer.MAJOR_KEYS:
            self.reset_semver()
            self.assertEqual(
                self.semver.__repr__(),
                '1.2.3'
            )
            self.semver.bump(component)
            self.assertEqual(
                self.semver.__repr__(),
                '2.0.0'
            )


@mark.parametrize(
    "first,second,result",
    [
        (1, 2, 1),
        (2, 1, -1),
        (1, 1, 0)
    ]
)
def test_compare_component(first, second, result):
    assert result == SemVer.compare_component(first, second)


class FromVersionUnitTests(SemVerTestCase):
    VERSION = '1.2.3'

    @patch(
        'gitflow_easyrelease.semver.is_semver',
        return_value=True
    )
    def test_with_semver_version(self, mock_is_semver):
        mock_is_semver.assert_not_called()
        result = SemVer.from_version(self.VERSION)
        mock_is_semver.assert_called_once_with(self.VERSION)
        self.assertEqual(
            result.__repr__(),
            self.VERSION
        )

    @patch(
        'gitflow_easyrelease.semver.is_semver',
        return_value=False
    )
    def test_without_semver_version(self, mock_is_semver):
        mock_is_semver.assert_not_called()
        result = SemVer.from_version(self.VERSION)
        mock_is_semver.assert_called_once_with(self.VERSION)
        self.assertEqual(
            result.__repr__(),
            '0.0.0'
        )


@mark.parametrize(
    "version,result",
    [
        (''.join(SemVer.ALL_KEYS), False),
        (SemVer.PATCH_KEYS[0], True)
    ]
)
def test_is_component(version, result):
    assert result == SemVer.is_component(version)


class GetActiveBranchUnitTests(SemVerTestCase):

    @patch(
        'gitflow_easyrelease.semver.RepoInfo.to_semver_args',
        return_value=None
    )
    def test_without_release_branch(self, mock_args):
        mock_args.assert_not_called()
        self.assertIsNone(SemVer.get_active_branch())
        mock_args.assert_called_once_with()

    @patch(
        'gitflow_easyrelease.semver.RepoInfo.to_semver_args',
        return_value=[1, 2, 3]
    )
    def test_with_release_branch(self, mock_args):
        mock_args.assert_not_called()
        self.assertEqual(
            SemVer.get_active_branch().__repr__(),
            '1.2.3'
        )
        mock_args.assert_called_once_with()


class GetCurrentVersionUnitTests(SemVerTestCase):

    RETURN_NONE = MagicMock(return_value=None)
    TAGS = [
        '0.0.0',
        '1.0.0',
        '0.1.0',
        '0.0.1'
    ]

    @patch(
        'gitflow_easyrelease.semver.SemVer.get_active_branch',
        return_value=SemVer(1, 2, 3)
    )
    def test_with_active_release_branch(self, mock_active):
        mock_active.assert_not_called()
        self.assertEqual(
            SemVer.get_current_version().__repr__(),
            '1.2.3'
        )
        mock_active.assert_called_once_with()

    @patch(
        'gitflow_easyrelease.semver.SemVer.get_active_branch',
        RETURN_NONE
    )
    @patch(
        'gitflow_easyrelease.semver.RepoInfo.get_semver_tags',
        RETURN_NONE
    )
    def test_no_versions(self):
        self.assertEqual(
            SemVer.get_current_version().__repr__(),
            '0.0.0'
        )

    @patch(
        'gitflow_easyrelease.semver.RepoInfo.get_semver_tags',
        return_value=TAGS
    )
    def test_tagged_versions(self, mock_tags):
        mock_tags.assert_not_called()
        self.assertEqual(
            SemVer.get_current_version().__repr__(),
            '1.0.0'
        )
        mock_tags.assert_called_once_with()


class ProcessVersionUnitTests(SemVerTestCase):
    """"""
