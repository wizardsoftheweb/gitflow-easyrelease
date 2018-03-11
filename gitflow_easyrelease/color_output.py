"""This file provides the ColorOutput class"""

from __future__ import print_function

from subprocess import CalledProcessError, check_output

from colors import color


class ColorOutput:

    def __init__(self, force_color=False, block_color=False):
        self.force_color = force_color
        self.block_color = block_color
        self.color = self.color_factory()

    def color_factory(self):
        if not self.block_color:
            if ColorOutput.can_use_ansi() or self.force_color:
                return color
        return ColorOutput.no_color

    def __call__(self, *args, **kwargs):
        return self.color(*args, **kwargs)

    @staticmethod
    def can_use_ansi():
        try:
            check_output(['which', 'tput'])
            colors = int(check_output(['tput', 'colors']).strip())
            if 8 <= colors:
                return True
        except CalledProcessError:
            pass
        return False

    @staticmethod
    def no_color(text_to_color, **kwargs):
        return text_to_color
