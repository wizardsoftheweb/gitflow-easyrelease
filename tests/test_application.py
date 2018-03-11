# pylint: disable=missing-docstring

from __future__ import print_function

from argparse import Namespace
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

    def setUp(self):
        ApplicationTestCase.setUp(self)
        create_root_parser_patcher = patch.object(
            Application,
            'create_root_parser',
            return_value=self.parser
        )
        self.mock_create_root_parser = create_root_parser_patcher.start()
        self.addCleanup(create_root_parser_patcher.stop)
        parse_args_patcher = patch(
            'gitflow_easyrelease.application.Application.parse_args',
            return_value=[MagicMock(spec=[]), MagicMock(spec=[])]
        )
        self.mock_parse_args = parse_args_patcher.start()
        self.addCleanup(parse_args_patcher.stop)
        populate_root_parser_patcher = patch.object(
            Application,
            'populate_root_parser'
        )
        self.mock_populate_root_parser = populate_root_parser_patcher.start()
        self.addCleanup(populate_root_parser_patcher.stop)
        print_all_help_patcher = patch(
            'gitflow_easyrelease.application.Application.print_all_help'
        )
        self.mock_print_all_help = print_all_help_patcher.start()
        self.addCleanup(print_all_help_patcher.stop)

    def test_print_all_help(self):
        parsed = Namespace()
        parsed.all_help = True
        options = []
        self.mock_parse_args.return_value = [parsed, options]
        self.mock_create_root_parser.assert_not_called()
        self.mock_parse_args.assert_not_called()
        self.mock_populate_root_parser.assert_not_called()
        self.mock_print_all_help.assert_not_called()
        self.mock_sub_execute.assert_not_called()
        self.application.bootstrap(['--all-help'])
        self.mock_create_root_parser.assert_called_once_with()
        self.mock_parse_args.assert_called_once_with(
            self.parser,
            ['--all-help']
        )
        self.mock_populate_root_parser.assert_called_once_with(self.parser)
        self.mock_print_all_help.assert_called_once_with(self.parser)
        self.mock_sub_execute.assert_not_called()

    def test_execute(self):
        parsed = Namespace()
        parsed.all_help = False
        parsed.subcommand = self.SUBCOMMAND_KEY
        options = ['--show-commands']
        final = Namespace()
        final.all_help = False
        final.subcommand = self.SUBCOMMAND_KEY
        final.options = options
        self.mock_parse_args.return_value = [parsed, options]
        self.mock_create_root_parser.assert_not_called()
        self.mock_parse_args.assert_not_called()
        self.mock_populate_root_parser.assert_not_called()
        self.mock_print_all_help.assert_not_called()
        self.mock_sub_execute.assert_not_called()
        self.application.bootstrap([self.SUBCOMMAND_KEY, '--show-commands'])
        self.mock_create_root_parser.assert_called_once_with()
        self.mock_parse_args.assert_has_calls([
            call(self.parser, [self.SUBCOMMAND_KEY, '--show-commands']),
            call(self.parser, [self.SUBCOMMAND_KEY, '--show-commands'])
        ])
        self.mock_populate_root_parser.assert_called_once_with(self.parser)
        self.mock_print_all_help.assert_not_called()
        self.mock_sub_execute.assert_called_once_with(final)


class CreateRootParserUnitTests(ApplicationTestCase):
    """"""


class ParseArgsUnitTests(ApplicationTestCase):
    """"""


class AllHelpProgHeaderUnitTests(ApplicationTestCase):
    """"""


class PrintAllHelpUnitTests(ApplicationTestCase):
    """"""
