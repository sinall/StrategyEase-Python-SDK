# -*- coding: utf-8 -*-

import logging
import os
import unittest

import six
from hamcrest import *
from requests import HTTPError
from six.moves import configparser

from strategyease_sdk import Client
from tests.strategyease_sdk.matchers.dataframe_matchers import *

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser


class ClientMarginTradingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)
        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read('{}/../config/config.ini'.format(dir_path))
        cls.client = Client(logging.getLogger(), **dict(config.items('StrategyEase')))
        cls.client_param = config.get('StrategyEase', 'client')

    def test_query(self):
        try:
            df = self.client.query(self.client_param, '融券卖出')
            assert_that(df, has_column(u'证券代码'))
        except HTTPError as e:
            self.fail()

    def test_buy_on_margin(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='BUY_ON_MARGIN', symbol='000001', type='LIMIT', price=9, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_buy_on_margin_at_market_price(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='BUY_ON_MARGIN', symbol='000001', type='MARKET', priceType=4, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_sell_then_repay(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='SELL_THEN_REPAY', symbol='000001', type='LIMIT', price=9.5, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_sell_then_repay_at_market_price(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='SELL_THEN_REPAY', symbol='000001', type='MARKET', priceType=4, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_sell_on_margin(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='SELL_ON_MARGIN', symbol='000003', type='LIMIT', price=9.5, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_sell_on_margin_at_market_price(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='SELL_ON_MARGIN', symbol='000001', type='MARKET', priceType=4, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_buy_then_repay(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='BUY_THEN_REPAY', symbol='000001', type='LIMIT', price=8.9, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_buy_then_repay_at_market_price(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='BUY_THEN_REPAY', symbol='000001', type='MARKET', priceType=4, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_repay_cash(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='REPAY_CASH', symbol='', type='LIMIT', price=1.0, amount=1
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")

    def test_repay_sec(self):
        try:
            order = self.client.execute(
                self.client_param,
                action='REPAY_SEC', symbol='000001', type='LIMIT', price=0.0, amount=100
            )
            self.assertIsNotNone(order['id'])
        except HTTPError as e:
            result = e.response.json()
            self.assertNotEqual(result['source'], "策略易")
