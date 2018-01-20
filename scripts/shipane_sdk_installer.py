#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs
import errno
import logging
import os
import re
import shutil
import sys
from datetime import datetime
from enum import Enum

import requests
import six

GIT_BASE_URL = "https://raw.githubusercontent.com/sinall/ShiPanE-Python-SDK"
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
        self._install_sdk()
        try:
            self._install_config()
        except:
            self._logger.error("无法安装配置文件")

    def _install_sdk(self):
        buffer = []
        module_statements = []
        main_module = "shipane_sdk.{0}.manager".format(self._quant)
        self._import_sdk_module(main_module, buffer, module_statements)

        output_file_path = os.path.join(self._output_dir, 'shipane_sdk.py')
        self._mkdir_p(os.path.dirname(output_file_path))
        self._backup(output_file_path)
        self._write_file(buffer, output_file_path)
        self._logger.info(u"生成文件[%s]成功", output_file_path)

    def _install_config(self):
        file_path = "config/online-quant/research/shipane_sdk_config_template.yaml"
        source_file = self._get_file(file_path)

        tpl_output_file_path = os.path.join(self._output_dir, 'shipane_sdk_config_template.yaml')
        self._backup(tpl_output_file_path)
        self._write_file(list(source_file), tpl_output_file_path)
        self._logger.info(u"生成文件[%s]成功", tpl_output_file_path)

        output_file_path = os.path.join(self._output_dir, 'shipane_sdk_config.yaml')
        if not os.path.isfile(output_file_path):
            shutil.copyfile(tpl_output_file_path, output_file_path)

    def _import_sdk_module(self, module, buffer, module_statements):
        path = module.replace('.', '/') + '.py'
        lines = list(self._get_file(path))
        if buffer and re.search("^#.*coding:", lines[0]):
            lines.pop(0)
        index = next(i for i, line in enumerate(lines) if line and not line.isspace())
        for line in lines[index:]:
            match = re.search("^from .* import .*", line) or re.search("^import .*", line)
            if match:
                if line in module_statements:
                    continue
                self._import_module(line, buffer, module_statements)
                module_statements.append(line)
            else:
                buffer.append(line)

    def _import_module(self, statement, buffer, module_statements):
        match = re.search("^from __future__ import .*", statement)
        if match:
            index = next(i for i, line in enumerate(buffer) if line.startswith("# End   of __future__ module"))
            buffer.insert(index, statement)
            return
        match = re.search("^from (?!shipane_sdk).* import .*", statement) or re.search("^import .*", statement)
        if match:
            index = next(i for i, line in enumerate(buffer) if line.startswith("# End   of external module"))
            buffer.insert(index, statement)
            return
        match = re.search("^from (shipane_sdk\\..*) import .*", statement)
        if match:
            module = match.group(1)
            self._import_sdk_module(module, buffer, module_statements)
            return

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
        url = "{0}/{1}/{2}".format(GIT_BASE_URL, self._version, path)
        response = requests.get(url)
        response.raise_for_status()
        file = six.StringIO(response.text)
        return file

    def _backup(self, filename):
        backup_dir = os.path.join(self._output_dir, 'backup')
        self._mkdir_p(backup_dir)

        if not os.path.isfile(filename):
            return

        filename_parts = os.path.splitext(os.path.basename(filename))
        backup_filename = "{0}/{1}.{2}.{3}".format(
            backup_dir, filename_parts[0], datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), filename_parts[1]
        )
        shutil.copyfile(filename, backup_filename)
        self._logger.info(u"备份文件[%s]至[%s]成功", filename, backup_filename)

    def _mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _write_file(self, buffer, path):
        with codecs.open(path, "w+", "utf-8") as file:
            for line in buffer:
                file.write(line)


def main(args):
    logging.basicConfig(level=logging.DEBUG)

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
