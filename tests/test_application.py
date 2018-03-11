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
        ensure_git_flow_patcher = patch(
            'gitflow_easyrelease.application.RepoInfo.ensure_git_flow',
            return_value=True
        )
        self.mock_ensure_git_flow = ensure_git_flow_patcher.start()
        self.addCleanup(ensure_git_flow_patcher.stop)
        self.application = Application()


class ConstructorUnitTests(ApplicationTestCase):

    def test_flow(self):
        self.mock_ensure_git_flow.assert_called_once_with()


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
