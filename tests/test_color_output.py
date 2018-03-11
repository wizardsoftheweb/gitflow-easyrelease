# pylint: disable=missing-docstring

from __future__ import print_function

from unittest import TestCase

from mock import call, MagicMock, patch

from gitflow_easyrelease import ColorOutput


class ColorOutputTestCase(TestCase):

    def setUp(self):
        self.construct_color_output()
        self.addCleanup(self.wipe_color_output)

    def wipe_color_output(self):
        del self.color_output

    def construct_color_output(self):
        color_factory_patcher = patch.object(ColorOutput, 'color_factory')
        self.mock_color_factory = color_factory_patcher.start()
        self.color_output = ColorOutput()
        color_factory_patcher.stop()


class ConstructorUnitTests(ColorOutputTestCase):

    def test_call(self):
        self.mock_color_factory.assert_called_once_with()


class ColorFactoryUnitTests(ColorOutputTestCase):
    """"""


class CallUnitTests(ColorOutputTestCase):
    """"""


class CanUseAnsiUnitTests(ColorOutputTestCase):
    """"""


class NoColorUnitTests(ColorOutputTestCase):
    """"""
