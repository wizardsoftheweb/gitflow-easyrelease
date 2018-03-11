# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from gitflow_easyrelease import Application


class ApplicationTestCase(TestCase):

    def setUp(self):
        self.construct_application()
        self.addCleanup(self.wipe_application)

    def wipe_application(self):
        del self.application

    def construct_application(self):
        self.application = Application()


class ConstructorUnitTests(ApplicationTestCase):
    """"""


class AttachSubparsersUnitTests(ApplicationTestCase):
    """"""


class PopulateRootParserUnitTests(ApplicationTestCase):
    """"""


class BootstrapUnitTests(ApplicationTestCase):
    """"""


class CreateRootParserUnitTests(ApplicationTestCase):
    """"""


class ParseArgsUnitTests(ApplicationTestCase):
    """"""


class AllHelpProgHeaderUnitTests(ApplicationTestCase):
    """"""


class PrintAllHelpUnitTests(ApplicationTestCase):
    """"""
