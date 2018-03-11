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
    """"""


class CompareUnitTests(SemVerTestCase):
    """"""


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
