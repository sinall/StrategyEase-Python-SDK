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

from shipane_sdk.joinquant.client import JoinQuantClient


class JoinQuantClientTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.readfp(codecs.open('{}/../../config/config.ini'.format(dir_path), encoding="utf_8_sig"))
        self._jq_client = JoinQuantClient(**dict(config.items('JoinQuant')))

    def test_query(self):
        self._jq_client.login()
        transactions = self._jq_client.query()
        self.assertTrue(isinstance(transactions, list))

    def test_query_portfolio(self):
        self._jq_client.login()
        portfolio = self._jq_client.query_portfolio()
        self.assertIsNotNone(portfolio)
