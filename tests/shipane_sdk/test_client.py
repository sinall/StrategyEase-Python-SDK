# -*- coding: utf-8 -*-

import inspect
import os
import unittest

import six
from six.moves import configparser

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser

from shipane_sdk import Client


class ClientTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../config/config.ini'.format(dir_path))
        self.client = Client(host=config.get('ShiPanE', 'host'))

    def test_get_account(self):
        response = self.client.get_account()
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)

    def test_get_positions(self):
        response = self.client.get_positions()
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)

    def test_buy_stock(self):
        response = self.client.buy(symbol='000001', price=8.11, amount=100)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        json = response.json();
        if response.status_code == 200:
            self.assertTrue(json['id'])
        elif response.status_code == 400:
            self.assertTrue(json['message'])
        else:
            self.fail()

    def test_sell_stock(self):
        response = self.client.sell(symbol='000001', price=9.51, amount=100)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        json = response.json();
        if response.status_code == 200:
            self.assertTrue(json['id'])
        elif response.status_code == 400:
            self.assertTrue(json['message'])
        else:
            self.fail()

    def test_cancel_all(self):
        response = self.client.cancel_all()
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)

    def test_query(self):
        response = self.client.query(None, '查询>资金股份')
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)
