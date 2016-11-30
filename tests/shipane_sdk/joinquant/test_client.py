# -*- coding: utf-8 -*-

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
        config.read('{}/../../config/config.ini'.format(dir_path))
        self._jqClient = JoinQuantClient(username=config.get('JoinQuant', 'username'),
                                         password=config.get('JoinQuant', 'password'),
                                         backtest_id=config.get('JoinQuant', 'backtestId'))

    def test_query(self):
        self._jqClient.login()
        transaction_detail = self._jqClient.query()
        self.assertTrue(transaction_detail.has_key('data'))
