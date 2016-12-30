# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path
import os.path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='shipane_sdk',

    version='1.0.0.a9',

    description=u'实盘易（ShiPanE）Python SDK，通达信自动化交易 API。',
    long_description=long_description,

    url='https://github.com/sinall/ShiPanE-Python-SDK',

    author='sinall',
    author_email='gaoruinan@163.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='ShiPanE SDK 通达信 TDX Automation',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests', 'six', 'apscheduler', 'lxml', 'cssselect', 'bs4', 'html5lib', 'pandas', 'rqopen-client'],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
    },

    data_files=[(os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config'), ['config/scheduler-example.ini'])],

    scripts=['scripts/shipane-scheduler.py'],

    entry_points={
        'console_scripts': [
        ],
    },
)
