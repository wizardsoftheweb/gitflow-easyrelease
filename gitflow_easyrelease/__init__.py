"""This file provides the gitflow_easyrelease module"""

from .semver import SemVer
from .repo_info import RepoInfo
from .color_output import ColorOutput
from .subcommand import Subcommand
from .application import Application
from .cli import cli

if '__main__' == __name__:
    cli()
