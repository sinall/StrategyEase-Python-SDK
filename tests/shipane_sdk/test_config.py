# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import codecs
import unittest

from shipane_sdk.support import *


class ConfigTest(unittest.TestCase):
    def test_parse(self):
        filename = "../../config/joinquant/research/shipane_sdk_config_template.yaml"
        with codecs.open(filename, encoding="utf_8_sig") as stream:
            config = yaml.load(stream, Loader=OrderedDictYAMLLoader)
            print(config)
