# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from gitflow_easyrelease import Subcommand


class SubcommandTestCase(TestCase):

    def setUp(self):
        self.construct_subcommand()
        self.addCleanup(self.wipe_subcommand)

    def wipe_subcommand(self):
        del self.subcommand

    def construct_subcommand(self):
        self.subcommand = Subcommand()


class ConstructorUnitTests(SubcommandTestCase):

    def test_without_release_commands(self):
        self.assertEqual(
            self.subcommand.release_commands,
            []
        )


class AttachSubparserUnitTests(SubcommandTestCase):

    def setUp(self):
        SubcommandTestCase.setUp(self)
        self.subcommand.has_version = False
        self.subcommand.version_optional = True
        self.subcommand.has_base = False
        self.parser = MagicMock()
        self.mock_add = MagicMock(return_value=self.parser)
        self.subparsers = MagicMock(add_parser=self.mock_add)
        attach_version_argument_patcher = patch.object(
            Subcommand,
            'attach_version_argument'
        )
        self.mock_attach_version_argument = attach_version_argument_patcher.start()
        self.addCleanup(attach_version_argument_patcher.stop)
        attach_base_argument_patcher = patch.object(
            Subcommand,
            'attach_base_argument'
        )
        self.mock_attach_base_argument = attach_base_argument_patcher.start()
        self.addCleanup(attach_base_argument_patcher.stop)

    def test_parser_only(self):
        self.mock_add.assert_not_called()
        self.mock_attach_version_argument.assert_not_called()
        self.mock_attach_base_argument.assert_not_called()
        self.subcommand.attach_subparser(self.subparsers)
        self.mock_add.assert_called_once()
        self.mock_attach_version_argument.assert_not_called()
        self.mock_attach_base_argument.assert_not_called()

    def test_version(self):
        self.subcommand.has_version = True
        self.subcommand.version_optional = True
        self.mock_add.assert_not_called()
        self.mock_attach_version_argument.assert_not_called()
        self.mock_attach_base_argument.assert_not_called()
        self.subcommand.attach_subparser(self.subparsers)
        self.mock_add.assert_called_once()
        self.mock_attach_version_argument.assert_called_once_with(
            self.parser,
            True
        )
        self.mock_attach_base_argument.assert_not_called()

    def test_base(self):
        self.subcommand.has_base = True
        self.mock_add.assert_not_called()
        self.mock_attach_version_argument.assert_not_called()
        self.mock_attach_base_argument.assert_not_called()
        self.subcommand.attach_subparser(self.subparsers)
        self.mock_add.assert_called_once()
        self.mock_attach_version_argument.assert_not_called()
        self.mock_attach_base_argument.assert_called_once_with(self.parser)


class ExecuteUnitTests(SubcommandTestCase):
    VERSION = MagicMock()
    BASE_BRANCH = 'qqq'
    OPTIONS = '--show-commands'
    RELEASE_COMMANDS = ['one']

    def setUp(self):
        SubcommandTestCase.setUp(self)
        self.subcommand.release_commands = self.RELEASE_COMMANDS
        execute_release_command_patcher = patch.object(
            Subcommand,
            'execute_release_command'
        )
        self.mock_execute_release_command = execute_release_command_patcher.start()
        self.addCleanup(execute_release_command_patcher.stop)

    @patch(
        'gitflow_easyrelease.subcommand.SemVer.process_version',
        return_value=None
    )
    def test_missing_version(self, mock_process):
        self.subcommand.has_version = True
        mock_process.assert_not_called()
        self.mock_execute_release_command.assert_not_called()
        with self.assertRaises(ValueError):
            self.subcommand.execute(MagicMock(version=None, spec=['version']))
            mock_process.assert_called_once_with(None)
            self.mock_execute_release_command.assert_not_called()

    @patch(
        'gitflow_easyrelease.subcommand.SemVer',
        return_value=VERSION
    )
    def test_valid_version(self, mock_semver):
        mock_semver.assert_not_called()
        self.mock_execute_release_command.assert_not_called()
        self.subcommand.execute(MagicMock(spec=[]))
        mock_semver.assert_called_once_with()
        self.mock_execute_release_command.assert_has_calls([
            call(self.RELEASE_COMMANDS[0], self.VERSION, None, None)
        ])

    @patch(
        'gitflow_easyrelease.subcommand.SemVer',
        MagicMock(return_value=VERSION)
    )
    def test_with_base(self):
        self.mock_execute_release_command.assert_not_called()
        self.subcommand.execute(MagicMock(
            base=self.BASE_BRANCH,
            spec=['base']
        ))
        self.mock_execute_release_command.assert_has_calls([
            call(self.RELEASE_COMMANDS[0], self.VERSION, 'qqq', None)
        ])

    @patch(
        'gitflow_easyrelease.subcommand.SemVer',
        MagicMock(return_value=VERSION)
    )
    def test_with_options(self):
        self.mock_execute_release_command.assert_not_called()
        self.subcommand.execute(MagicMock(
            options=self.OPTIONS,
            spec=['options']
        ))
        self.mock_execute_release_command.assert_has_calls([
            call(self.RELEASE_COMMANDS[0], self.VERSION, None, self.OPTIONS)
        ])


class AttachVersionArgumentUnitTests(SubcommandTestCase):
    COLOR = MagicMock()

    def setUp(self):
        SubcommandTestCase.setUp(self)
        color_output_patcher = patch(
            'gitflow_easyrelease.subcommand.ColorOutput',
            return_value=self.COLOR
        )
        self.mock_color_output = color_output_patcher.start()
        self.addCleanup(color_output_patcher.stop)
        self.mock_add = MagicMock()
        self.parser = MagicMock(add_argument=self.mock_add)

    def test_color_output(self):
        self.mock_color_output.assert_not_called()
        Subcommand.attach_version_argument(
            self.parser,
            self.subcommand.version_optional
        )
        self.mock_color_output.assert_called_once_with()

    def test_add_call(self):
        self.mock_add.assert_not_called()
        Subcommand.attach_version_argument(
            self.parser,
            self.subcommand.version_optional
        )
        self.mock_add.assert_called_once()


class AttachBaseArgumentUnitTests(SubcommandTestCase):

    def setUp(self):
        SubcommandTestCase.setUp(self)
        self.mock_add = MagicMock()
        self.parser = MagicMock(add_argument=self.mock_add)

    def test_add_call(self):
        self.mock_add.assert_not_called()
        Subcommand.attach_base_argument(self.parser)
        self.mock_add.assert_called_once()


class ExecuteReleaseCommandUnitTests(SubcommandTestCase):
    """"""
