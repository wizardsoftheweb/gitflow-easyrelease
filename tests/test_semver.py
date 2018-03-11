# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

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
    """"""


class LesserUnitTests(SemVerTestCase):
    """"""


class EqualUnitTests(SemVerTestCase):
    """"""


class BumpUnitTests(SemVerTestCase):
    """"""


class ReprUnitTests(SemVerTestCase):
    """"""


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
