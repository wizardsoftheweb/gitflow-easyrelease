# pylint: disable=missing-docstring

from __future__ import print_function

from collections import OrderedDict
from unittest import TestCase

from mock import call, MagicMock, patch

from gitflow_easyrelease import Application


class ApplicationTestCase(TestCase):
    SUBCOMMAND_KEY = 'quick'

    def setUp(self):
        self.construct_application()
        self.addCleanup(self.wipe_application)
        self.subparsers = MagicMock()
        self.mock_parser_add = MagicMock(return_value=self.subparsers)
        self.parser = MagicMock(
            add_subparsers=self.mock_parser_add,
            add_argument=self.mock_parser_add
        )

    def wipe_application(self):
        del self.application

    def construct_application(self):
        ensure_git_flow_patcher = patch(
            'gitflow_easyrelease.application.RepoInfo.ensure_git_flow',
            return_value=True
        )
        self.mock_ensure_git_flow = ensure_git_flow_patcher.start()
        self.addCleanup(ensure_git_flow_patcher.stop)
        self.mock_sub_attach = MagicMock()
        self.mock_sub_execute = MagicMock()
        subcommands = OrderedDict({
            self.SUBCOMMAND_KEY: MagicMock(
                attach_subparser=self.mock_sub_attach,
                execute=self.mock_sub_execute
            )
        })
        self.application = Application(subcommands)


class ConstructorUnitTests(ApplicationTestCase):

    def test_flow(self):
        self.mock_ensure_git_flow.assert_called_once_with()


class AttachSubparsersUnitTests(ApplicationTestCase):

    def test_subparser_add(self):
        self.mock_parser_add.assert_not_called()
        self.application.attach_subparsers(self.parser)
        self.mock_parser_add.assert_called_once()

    def test_subcommand_attach(self):
        self.mock_sub_attach.assert_not_called()
        self.application.attach_subparsers(self.parser)
        self.mock_sub_attach.assert_called_once_with(self.subparsers)


class PopulateRootParserUnitTests(ApplicationTestCase):

    def setUp(self):
        ApplicationTestCase.setUp(self)
        attach_subparsers_patcher = patch.object(
            Application,
            'attach_subparsers'
        )
        self.mock_attach_subparsers = attach_subparsers_patcher.start()
        self.addCleanup(attach_subparsers_patcher.stop)

    def test_argument_add(self):
        self.mock_parser_add.assert_not_called()
        self.application.populate_root_parser(self.parser)
        self.mock_parser_add.assert_called_once()

    def test_subparsers_add(self):
        self.mock_attach_subparsers.assert_not_called()
        self.application.populate_root_parser(self.parser)
        self.mock_attach_subparsers.assert_called_once()


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
