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


class ClientTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../config/config.ini'.format(dir_path))
        self.client = Client(logging.getLogger(), host=config.get('ShiPanE', 'host'), key=config.get('ShiPanE', 'key'))
        self.client.start_clients()

    def test_get_account(self):
        try:
            self.client.get_account()
        except HTTPError as e:
            self.fail()

    def test_get_positions(self):
        try:
            data = self.client.get_positions()
            sub_accounts = data['sub_accounts']
            self.assertGreater(sub_accounts['总资产']['人民币'], 0)
            positions = data['positions']
            self.assertIsNotNone(positions['证券代码'][0])
        except HTTPError as e:
            self.fail()

    def test_buy_stock(self):
        try:
            order = self.client.buy(symbol='000001', price=8.11, amount=100)
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertIsNotNone(result['message'])

    def test_sell_stock(self):
        try:
            order = self.client.sell(symbol='000001', price=9.51, amount=100)
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertIsNotNone(result['message'])

    def test_cancel_all(self):
        try:
            self.client.cancel_all()
        except HTTPError as e:
            self.fail()

    def test_query(self):
        try:
            df = self.client.query(None, '查询>资金股份')
            self.assertIsNotNone(df['证券代码'][0])
        except HTTPError as e:
            self.fail()

    def test_query_new_stocks(self):
        df = self.client.query_new_stocks()
        self.assertTrue((df.columns == ['code', 'xcode', 'name', 'ipo_date', 'price']).all())
