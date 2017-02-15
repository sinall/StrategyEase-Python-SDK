# -*- coding: utf-8 -*-
import codecs
import os
import unittest

import six
from six.moves import configparser

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser

from shipane_sdk.uqer.client import UqerClient


class UqerClientTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.readfp(codecs.open('{}/../../config/config.ini'.format(dir_path), encoding="utf_8_sig"))
        self._uq_client = UqerClient(**dict(config.items('Uqer')))

    def test_query(self):
        self._uq_client.login()
        transactions = self._uq_client.query()
        self.assertTrue(isinstance(transactions, list))
