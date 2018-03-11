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
    """"""


class AttachVersionArgumentUnitTests(SubcommandTestCase):
    """"""


class AttachBaseArgumentUnitTests(SubcommandTestCase):
    """"""


class ExecuteReleaseCommandUnitTests(SubcommandTestCase):
    """"""
