# -*- coding: utf-8 -*-
import json
import os
import unittest
from datetime import datetime

from shipane_sdk.joinquant.transaction import JoinQuantTransaction


class TransactionTest(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open('{}/../../sample_data/transactionDetail.json'.format(dir_path)) as data_file:
            self._transaction_detail = json.loads(data_file.read())

    def test_from_raw(self):
        jq_transaction = JoinQuantTransaction(self._transaction_detail['data']['transaction'][0])
        transaction = jq_transaction.normalize()
        self.assertEqual(transaction.completed_at, datetime.strptime('2016-11-22 09:30', '%Y-%m-%d %H:%M'))
        self.assertEqual(transaction.action, 'BUY')
        self.assertEqual(transaction.symbol, '000001')
        self.assertEqual(transaction.price, 9.25)
        self.assertEqual(transaction.amount, 100)
