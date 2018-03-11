# pylint: disable=missing-docstring

from __future__ import print_function


from mock import patch

from gitflow_easyrelease import cli


@patch('gitflow_easyrelease.cli_file.ColorOutput')
@patch('gitflow_easyrelease.cli_file.Subcommand')
@patch('gitflow_easyrelease.cli_file.Application')
def test_execution(mock_app, mock_sub, mock_color):
    mock_color.assert_not_called()
    mock_sub.assert_not_called()
    mock_app.assert_not_called()
    cli()
    mock_color.assert_called_once()
    assert 1 <= mock_sub.call_count
    mock_app.assert_called_once()
