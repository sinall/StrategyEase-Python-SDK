# -*- coding: utf-8 -*-

import codecs
import os
import unittest

from six.moves import configparser

from strategyease_sdk.guorn.client import GuornClient

ConfigParser = configparser.RawConfigParser


class GuornClientTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.readfp(codecs.open('{}/../../config/config.ini'.format(dir_path), encoding="utf_8_sig"))
        self._guorn_client = GuornClient(**dict(config.items('Guorn')))
        self._guorn_client.login()

    def test_query_portfolio(self):
        portfolio = self._guorn_client.query_portfolio()
        print(portfolio)
