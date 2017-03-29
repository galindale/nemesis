# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import os

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.md'), encoding='utf-8').read()

setup(
    # Package info
    name='nemesis',
    version='0.1.0',
    description='Slackbot that track the happiness of your team',
    author='Sergio Zamarro, Alba Cañas',
    author_email='sergiozam13@gmail.com, alba.caon@gmail.com',
    url='',
    long_description=readme,

    # Package classifiers
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    # Package structure
    packages=find_packages('backend', exclude=['ez_setup', '*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'': 'backend'},
    include_package_data=True,
    zip_safe=False,

    # Dependencies
    install_requires=open('requirements.txt', 'r').read().splitlines(),
    entry_points={
        'console_scripts': [
            'nemesis_bot = nemesis.bot.__main__:main',
            'nemesis_api = nemesis.api.__main__:main',
        ],
    }
)
