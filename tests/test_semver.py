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


@mark.parametrize(
    "version,result",
    [
        (''.join(SemVer.ALL_KEYS), False),
        (SemVer.PATCH_KEYS[0], True)
    ]
)
def test_is_component(version, result):
    assert result == SemVer.is_component(version)


class CompareComponentUnitTests(SemVerTestCase):
    """"""


class FromVersionUnitTests(SemVerTestCase):
    """"""


class IsComponentUnitTests(SemVerTestCase):
    """"""


class GetActiveBranchUnitTests(SemVerTestCase):
    """"""


class GetCurrentVersionUnitTests(SemVerTestCase):
    """"""


class ProcessVersionUnitTests(SemVerTestCase):
    """"""
