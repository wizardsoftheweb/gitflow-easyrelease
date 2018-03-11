"""This file sets up the package"""

from setuptools import setup

setup(
    name='gitflow-easyrelease',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'git-easyrelease = gitflow_easyrelease.cli_file:cli'
        ]
    }
)
