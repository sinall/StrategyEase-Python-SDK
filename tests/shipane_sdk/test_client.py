# -*- coding: utf-8 -*-

import logging
import os
import unittest

import six
from hamcrest import *
from requests import HTTPError
from six.moves import configparser

from shipane_sdk import Client
from shipane_sdk.client import MediaType
from tests.shipane_sdk.matchers.dataframe_matchers import *

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser


class ClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../config/config.ini'.format(dir_path))
        cls.client = Client(logging.getLogger(), **dict(config.items('ShiPanE')))
        cls.client_param = config.get('ShiPanE', 'client')

    def test_get_account(self):
        try:
            self.client.get_account(self.client_param)
        except HTTPError as e:
            self.fail()

    def test_get_positions(self):
        try:
            data = self.client.get_positions(self.client_param)
            assert_that(data['sub_accounts'], has_row(u'人民币'))
            assert_that(data['positions'], has_column(u'证券代码'))
        except HTTPError as e:
            self.fail()

    def test_get_positions_in_jq_format(self):
        try:
            data = self.client.get_positions(self.client_param, media_type=MediaType.JOIN_QUANT)
            self.assertIsNotNone(data['availableCash'])
        except HTTPError as e:
            self.fail()

    def test_get_orders(self):
        try:
            df = self.client.get_orders(self.client_param)
            assert_that(df, has_column_matches(u"(委托|合同)编号"))
        except HTTPError as e:
            self.fail()

    def test_get_open_orders(self):
        try:
            df = self.client.get_orders(self.client_param, 'open')
            assert_that(df, has_column_matches(u"(委托|合同)编号"))
        except HTTPError as e:
            self.fail()

    def test_get_filled_orders(self):
        try:
            df = self.client.get_orders(self.client_param, 'filled')
            assert_that(df, has_column_matches(u"(委托|合同)编号"))
        except HTTPError as e:
            self.fail()

    def test_buy_stock(self):
        try:
            order = self.client.buy(self.client_param, symbol='000001', price=9, amount=100)
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "实盘易")

    def test_sell_stock(self):
        try:
            order = self.client.sell(self.client_param, symbol='000001', price=9.5, amount=100)
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "实盘易")

    def test_buy_stock_at_market_price(self):
        try:
            order = self.client.buy(self.client_param, symbol='000001', type='MARKET', priceType=4, amount=100)
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "实盘易")

    def test_sell_stock_at_market_price(self):
        try:
            order = self.client.sell(self.client_param, symbol='000001', type='MARKET', priceType=4, amount=100)
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "实盘易")

    def test_cancel_all(self):
        try:
            self.client.cancel_all(self.client_param)
        except HTTPError as e:
            self.fail()

    def test_query(self):
        try:
            df = self.client.query(self.client_param, '查询>资金股份')
            assert_that(df, has_column(u'证券代码'))
        except HTTPError as e:
            self.fail()

    def test_query_new_stocks(self):
        df = self.client.query_new_stocks()
        self.assertTrue((df.columns == ['code', 'xcode', 'name', 'ipo_date', 'price']).all())

    def test_query_convertible_bonds(self):
        df = self.client.query_convertible_bonds()
        assert_that(df, has_column('ipo_date'))
        assert_that(df, has_column('xcode'))
