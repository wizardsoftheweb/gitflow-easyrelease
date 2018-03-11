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
    """"""


class AttachSubparserUnitTests(SubcommandTestCase):
    """"""


class ExecuteUnitTests(SubcommandTestCase):
    """"""


class AttachVersionArgumentUnitTests(SubcommandTestCase):
    """"""


class AttachBaseArgumentUnitTests(SubcommandTestCase):
    """"""


class ExecuteReleaseCommandUnitTests(SubcommandTestCase):
    """"""
