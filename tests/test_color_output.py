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
    COLOR = MagicMock()
    NO_COLOR = MagicMock()

    def setUp(self):
        ColorOutputTestCase.setUp(self)
        color_patcher = patch(
            'gitflow_easyrelease.color_output.color',
            self.COLOR
        )
        self.mock_color = color_patcher.start()
        self.addCleanup(color_patcher.stop)
        no_color_patcher = patch(
            'gitflow_easyrelease.color_output.ColorOutput.no_color',
            self.NO_COLOR
        )
        self.mock_no_color = no_color_patcher.start()
        self.addCleanup(no_color_patcher.stop)

    @patch(
        'gitflow_easyrelease.color_output.ColorOutput.can_use_ansi',
        return_value=True
    )
    def test_with_ansi_color(self, mock_ansi):
        mock_ansi.assert_not_called()
        result = self.color_output.color_factory()
        self.assertEqual(result, self.COLOR)
        mock_ansi.assert_called_once_with()

    @patch(
        'gitflow_easyrelease.color_output.ColorOutput.can_use_ansi',
        return_value=True
    )
    def test_blocked_color(self, mock_ansi):
        self.color_output.block_color = True
        mock_ansi.assert_not_called()
        result = self.color_output.color_factory()
        self.assertEqual(result, self.NO_COLOR)
        mock_ansi.assert_not_called()

    @patch(
        'gitflow_easyrelease.color_output.ColorOutput.can_use_ansi',
        return_value=False
    )
    def test_force_color(self, mock_ansi):
        self.color_output.force_color = True
        mock_ansi.assert_not_called()
        result = self.color_output.color_factory()
        self.assertEqual(result, self.COLOR)
        mock_ansi.assert_called_once_with()

    @patch(
        'gitflow_easyrelease.color_output.ColorOutput.can_use_ansi',
        return_value=False
    )
    def test_fall_through(self, mock_ansi):
        mock_ansi.assert_not_called()
        result = self.color_output.color_factory()
        self.assertEqual(result, self.NO_COLOR)
        mock_ansi.assert_called_once_with()


class CallUnitTests(ColorOutputTestCase):
    """"""


class CanUseAnsiUnitTests(ColorOutputTestCase):
    """"""


class NoColorUnitTests(ColorOutputTestCase):
    """"""
