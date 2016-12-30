# -*- coding: utf-8 -*-

import collections
import inspect
import logging
import os
import unittest

import six
from six.moves import configparser

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser

from shipane_sdk import JoinQuantExecutor


class JoinQuantExecutorTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../../config/config.ini'.format(dir_path))
        self.Order = collections.namedtuple('Order', ['is_buy', 'security', 'price', 'amount'])
        self.executor = JoinQuantExecutor(host=config.get('ShiPanE', 'host'))

    def test_buy_stock(self):
        mock_order = self.Order
        mock_order.is_buy = True
        mock_order.order_id = 1
        mock_order.security = '000001.XSHE'
        mock_order.price = 11.11
        mock_order.amount = 100
        response = self.executor.execute(mock_order)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        json = response.json();
        if response.status_code == 200:
            self.assertTrue(json['id'])
        elif response.status_code == 400:
            self.assertTrue(json['message'])
        else:
            self.fail()

    def test_sell_stock(self):
        mock_order = self.Order
        mock_order.is_buy = False
        mock_order.order_id = 2
        mock_order.security = '000001.XSHE'
        mock_order.price = 11.11
        mock_order.amount = 100
        response = self.executor.execute(mock_order)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        json = response.json();
        if response.status_code == 200:
            self.assertTrue(json['id'])
        elif response.status_code == 400:
            self.assertTrue(json['message'])
        else:
            self.fail()

    def test_cancel(self):
        mock_order = self.Order
        mock_order.is_buy = True
        mock_order.order_id = 3
        mock_order.security = '000001.XSHE'
        mock_order.price = 9.01
        mock_order.amount = 100
        self.executor.execute(mock_order)

        response = self.executor.cancel(mock_order)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        if response.status_code != 200:
            self.fail()
