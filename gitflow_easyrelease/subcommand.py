from __future__ import print_function

from argparse import ArgumentParser, REMAINDER
from collections import OrderedDict
from re import compile as re_compile, match
from subprocess import CalledProcessError, check_output
from sys import argv, exit as sys_exit

from argparse_color_formatter import ColorHelpFormatter
from colors import color

from gitflow_easyrelease import ColorOutput, SemVer


class Subcommand:

    def __init__(
            self,
            subcommand='',
            help_string='',
            release_commands=None,
            has_version=True,
            version_optional=True,
            has_base=True
    ):
        self.subcommand = subcommand
        self.help_string = help_string
        self.release_commands = (
            release_commands
            if release_commands
            else []
        )
        self.has_version = has_version
        self.version_optional = version_optional
        self.has_base = has_base

    def attach_subparser(self, subparsers):
        parser = subparsers.add_parser(
            self.subcommand,
            description=self.help_string,
            formatter_class=ColorHelpFormatter,
            help=self.help_string
        )
        if self.has_version:
            Subcommand.attach_version_argument(parser, self.version_optional)
        if self.has_base:
            Subcommand.attach_base_argument(parser)

    def execute(self, parsed_args):
        subcommand = parsed_args.subcommand
        version = (
            SemVer.process_version(parsed_args.version)
            if self.has_version
            else SemVer()
        )
        if version is None:
            raise Exception(
                'Version was not passed in and the repo is not on a release branch'
            )
        base = (
            parsed_args.base
            if self.has_base
            else None
        )
        options = parsed_args.options
        for command in self.release_commands:
            Subcommand.execute_release_command(command, version, base, options)

    @staticmethod
    def attach_version_argument(parser, version_optional=True):
        color_output = ColorOutput()
        options = {
            'help': (
                "The version to use."
                " %s, %s, and %s increment semver;"
                " anything else is used as the version string"
                % (
                    color_output('major', style='bold'),
                    color_output('minor', style='bold'),
                    color_output('patch', style='bold')
                )
            ),
            'type': str
        }
        if version_optional:
            options['nargs'] = '?'
        parser.add_argument('version', **options)

    @staticmethod
    def get_branches():
        return check_output([
            'git',
            'for-each-ref',
            '--format',
            '%(refname:short)',
            'refs/heads/',
            'refs/remotes/'
        ]).strip().split('\n')

    @staticmethod
    def attach_base_argument(parser):
        parser.add_argument(
            "base",
            nargs="?",
            default=None,
            help="Optional base branch",
            choices=Subcommand.get_branches(),
            type=str
        )

    @staticmethod
    def execute_release_command(command, version, base=None, options=None):
        command = ['git', 'flow', 'release', command, "%s" % version]
        if base:
            command.append(base)
        if options:
            command = command + options
        check_output(command)
