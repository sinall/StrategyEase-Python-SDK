# -*- coding: utf-8 -*-

import os
import unittest

import six
from six.moves import configparser

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser

from shipane_sdk.ricequant.client import RiceQuantClient


class RiceQuantClientTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../../config/config.ini'.format(dir_path))
        self._rqClient = RiceQuantClient(username=config.get('RiceQuant', 'username'),
                                         password=config.get('RiceQuant', 'password'),
                                         run_id=config.get('RiceQuant', 'run_id'))

    def test_query(self):
        self._rqClient.login()
        response = self._rqClient.query()
        self.assertTrue('resp' in response)
