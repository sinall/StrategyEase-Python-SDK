#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs
import logging
import os
import re
import shutil
import sys
from datetime import datetime
from enum import Enum

import requests
import six

GIT_BSAE_URL = "https://raw.githubusercontent.com/sinall/ShiPanE-Python-SDK"
WORK_DIR = '.'


class SourceLocation(Enum):
    LOCAL = "local"
    GITHUB = "github"


class SdkInstaller:
    def __init__(self, quant, output_dir, version, source_location):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._quant = quant
        self._output_dir = output_dir
        self._version = version
        self._source_location = source_location

    def install(self):
        path = "shipane_sdk/{0}/{1}".format(self._quant, 'executor.py')
        main_file = self._get_file(path)
        self._logger.info("获取文件[%s]成功", path)
        lines = list(main_file)
        buffer = []
        for line in lines:
            match = re.search("from (shipane_sdk\\..*) import .*", line)
            if match is None:
                buffer.append(line)
                continue
            module_name = match.group(1)
            self._append_module(buffer, module_name)
            self._logger.info("添加模块[%s]成功", module_name)

        output_filepath = os.path.join(self._output_dir, 'shipane_sdk.py')
        self._backup(output_filepath)
        with codecs.open(output_filepath, "w+", "utf-8") as sdk_file:
            for line in buffer:
                sdk_file.write(line)
        self._logger.info("生成文件[%s]成功", output_filepath)

    def _append_module(self, buffer, module):
        path = module.replace('.', '/') + '.py'
        lines = list(self._get_file(path))
        if re.search("^#.*coding:", lines[0]):
            lines.pop(0)
        buffer.append("\n")
        buffer.append("\n")
        buffer.append("# Begin of {0}\n".format(path))
        buffer.extend(lines)
        buffer.append("\n")
        buffer.append("\n")
        buffer.append("# End of {0}\n".format(path))

    def _get_file(self, path):
        if self._source_location is SourceLocation.LOCAL:
            file = self._get_local_file(path)
        else:
            file = self._get_url(path)
        return file

    def _get_local_file(self, path):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        source_root_dir = os.path.join(script_dir, "..")
        filename = os.path.join(source_root_dir, path)
        file = codecs.open(filename, encoding="utf-8")
        return file

    def _get_url(self, path):
        url = "{0}/{1}/{2}".format(GIT_BSAE_URL, self._version, path)
        response = requests.get(url)
        response.raise_for_status()
        file = six.StringIO(response.text)
        return file

    def _backup(self, filename):
        if not os.path.isfile(filename):
            return

        backup_dir = os.path.join(self._output_dir, 'backup')
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)
        filename_parts = os.path.splitext(os.path.basename(filename))
        backup_filename = "{0}/{1}.{2}.{3}".format(
            backup_dir, filename_parts[0], datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), filename_parts[1]
        )
        shutil.copyfile(filename, backup_filename)
        self._logger.info("备份文件[%s]至[%s]成功", filename, backup_filename)


def main(args):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--quant', help='在线量化平台名称，可选：joinquant、ricequant、uqer')
    parser.add_argument('--output', help='生成文件存储位置', default=WORK_DIR)
    parser.add_argument('--version', help='版本，如：v1.1.0.a6，默认为最新版本', default='master')
    parser.add_argument('--source-location', help='源代码位置，可选：local、github；默认为 github', default='github')
    args = parser.parse_known_args(args)

    sdk_installer = SdkInstaller(
        quant=args[0].quant,
        output_dir=args[0].output,
        version=args[0].version,
        source_location=SourceLocation(args[0].source_location)
    )
    sdk_installer.install()


if __name__ == "__main__":
    main(sys.argv[1:])
