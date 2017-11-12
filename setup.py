# -*- coding: utf-8 -*-

import os
import re
import shutil
from codecs import open

from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        config_path = os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config')
        ConfigInstantiator.instantiate(config_path)


class ConfigInstantiator:
    @staticmethod
    def instantiate(path):
        for filename in os.listdir(path):
            match = re.search("(.*)-template\\.(.*)", filename)
            if match is None:
                continue
            concrete_filename = '{}.{}'.format(match.group(1), match.group(2))
            template_file_path = os.path.join(path, filename)
            concrete_file_path = os.path.join(path, concrete_filename)
            if os.path.isfile(concrete_file_path):
                continue
            shutil.copyfile(template_file_path, concrete_file_path)


def main():
    here = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name='shipane_sdk',

        version='1.3.0a1',

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

        install_requires=['requests', 'six', 'apscheduler', 'lxml', 'cssselect', 'bs4', 'html5lib', 'pandas',
                          'rqopen-client', 'tushare', 'pyyaml'],

        extras_require={
            'dev': [],
            'test': [],
        },

        package_data={
        },

        data_files=[(os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config'), [
            'config/scheduler-template.ini',
            'config/logging-template.ini',
        ])],

        scripts=['scripts/shipane-scheduler.py'],

        entry_points={
            'console_scripts': [
                'shipane-scheduler = shipane_sdk.scheduler:start',
            ],
        },

        cmdclass={
            'install': CustomInstallCommand,
        },
    )


if __name__ == '__main__':
    main()
