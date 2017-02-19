# -*- coding: utf-8 -*-

import logging
import os
import unittest

import six
from requests import HTTPError
from six.moves import configparser

from shipane_sdk import Client

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser


class ClientManagementTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../config/config.ini'.format(dir_path))
        self.client = Client(logging.getLogger(), host=config.get('ShiPanE', 'host'), key=config.get('ShiPanE', 'key'))

    def test_start_clients(self):
        try:
            self.client.start_clients()
        except HTTPError as e:
            self.fail()

    def test_shutdown_clients(self):
        try:
            self.client.shutdown_clients()
        except HTTPError as e:
            self.fail()
