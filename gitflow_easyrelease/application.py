"""This file provides the Application class"""

from __future__ import print_function

from argparse import ArgumentParser
from collections import OrderedDict
from subprocess import check_output
from sys import argv, exit as sys_exit

from argparse_color_formatter import ColorHelpFormatter


class Application:
    """
    This class parses arguments and performs the desired action.
    """

    def __init__(self, subcommands=None):
        Application.ensure_git_flow()
        self.subcommands = (
            subcommands
            if subcommands
            else OrderedDict()
        )

    def attach_subparsers(self, parser):
        subparsers = parser.add_subparsers(
            dest='subcommand',
            help='Available subcommands'
        )
        for _, subcommand in self.subcommands.items():
            subcommand.attach_subparser(subparsers)

    def populate_root_parser(self, parser):
        parser.add_argument(
            '-h', '--help',
            action='help',
            help='show this help message and exit'
        )
        self.attach_subparsers(parser)

    def bootstrap(self, args=None):
        parser = self.create_root_parser()
        parsed_args = Application.parse_args(
            parser,
            (
                args
                if args
                else argv[1:]
            )
        )[0]
        self.populate_root_parser(parser)
        if parsed_args.all_help:
            Application.print_all_help(parser)
        else:
            parsed_args, options = Application.parse_args(
                parser,
                (
                    args
                    if args
                    else argv[1:]
                )
            )
            setattr(parsed_args, 'options', options)
            self.subcommands[parsed_args.subcommand].execute(parsed_args)

    @staticmethod
    def ensure_git_flow():
        check_output(['which', 'git-flow'])

    @staticmethod
    def create_root_parser():
        parser = ArgumentParser(
            description='A tool to simplify git-flow-release',
            formatter_class=ColorHelpFormatter,
            add_help=False
        )
        parser.add_argument(
            '--all-help',
            dest='all_help',
            action='store_true',
            help='Prints all available help'
        )
        return parser

    @staticmethod
    def parse_args(parser=None, args=None):
        if not args:
            args = ['-h']
        return parser.parse_known_args(args)

    @staticmethod
    def all_help_prog_header(parser):
        color_output = ColorOutput()
        return color_output(parser.prog, fg='green', style='bold+underline')

    @staticmethod
    def print_all_help(parser, in_color=False):
        print("%s\n" % Application.all_help_prog_header(parser))
        parser.print_help()
        if (
                parser
                and
                hasattr(parser, '_subparsers')
                and
                hasattr(parser._subparsers, '_actions')
        ):
            for action in [
                    action
                    for action in parser._subparsers._actions
                    if action.choices
            ]:
                for _, value in action.choices.items():
                    print("\n%s\n" % Application.all_help_prog_header(value))
                    value.print_help()
        sys_exit(0)
