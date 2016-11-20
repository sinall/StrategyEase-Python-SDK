# -*- coding: utf-8 -*-

import inspect
import unittest

import shipane_sdk


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = shipane_sdk.Client(host='192.168.1.102')

    def test_get_account(self):
        response = self.client.get_account()
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)

    def test_get_positions(self):
        response = self.client.get_positions()
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)

    def test_buy_stock(self):
        response = self.client.buy('000001', 8.11, 100)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        json = response.json();
        if (response.status_code == 200):
            self.assertTrue(json['id'])
        elif (response.status_code == 400):
            self.assertTrue(json['message'])
        else:
            self.fail()

    def test_sell_stock(self):
        response = self.client.sell('000001', 9.51, 100)
        print(inspect.stack()[0][3] + ' - ' + response.text)
        json = response.json();
        if (response.status_code == 200):
            self.assertTrue(json['id'])
        elif (response.status_code == 400):
            self.assertTrue(json['message'])
        else:
            self.fail()

    def test_cancel_all(self):
        response = self.client.cancel_all()
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)

    def test_query(self):
        response = self.client.query(navigation='查询>资金股份')
        print(inspect.stack()[0][3] + ' - ' + response.text)
        self.assertEqual(response.status_code, 200)
