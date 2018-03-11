from os.path import join
from setuptools import setup, find_packages

setup(
    name='gitflow-easyrelease',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'git-easyrelease = gitflow_easyrelease.cli:cli'
        ]
    }
)
