# -*- coding: utf-8 -*-
import json
import os
import unittest
from datetime import datetime

from shipane_sdk.joinquant.transaction import JoinQuantTransaction


class TransactionTest(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open('{}/../../sample_data/transactionDetail.json'.format(dir_path), encoding='utf_8_sig') as data_file:
            self._transaction_detail = json.loads(data_file.read())

    def test_from_raw(self):
        jq_transaction1 = JoinQuantTransaction(self._transaction_detail['data']['transaction'][0])
        transaction1 = jq_transaction1.normalize()
        self.assertEqual(transaction1.completed_at, datetime.strptime('2017-06-01 14:55', '%Y-%m-%d %H:%M'))
        self.assertEqual(transaction1.action, 'BUY')
        self.assertEqual(transaction1.symbol, '000001')
        self.assertEqual(transaction1.type, 'MARKET')
        self.assertEqual(transaction1.priceType, 4)
        self.assertEqual(transaction1.price, 9.19)
        self.assertEqual(transaction1.amount, 100)

        jq_transaction2 = JoinQuantTransaction(self._transaction_detail['data']['transaction'][1])
        transaction2 = jq_transaction2.normalize()
        self.assertEqual(transaction2.completed_at, datetime.strptime('2017-06-01 14:55', '%Y-%m-%d %H:%M'))
        self.assertEqual(transaction2.action, 'BUY')
        self.assertEqual(transaction2.symbol, '000002')
        self.assertEqual(transaction2.type, 'LIMIT')
        self.assertEqual(transaction2.priceType, 0)
        self.assertEqual(transaction2.price, 19.13)
        self.assertEqual(transaction2.amount, 100)
