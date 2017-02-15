# -*- coding: utf-8 -*-
import json
import os
import unittest
from datetime import datetime

from shipane_sdk.uqer.transaction import UqerTransaction


class TransactionTest(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open('{}/../../sample_data/uqer-order-response.json'.format(dir_path), 'r',
                  encoding='utf_8_sig') as data_file:
            self._transaction_detail = json.loads(data_file.read())

    def test_from_raw(self):
        uq_transaction = UqerTransaction(self._transaction_detail[0])
        transaction = uq_transaction.normalize()
        self.assertEqual(transaction.completed_at,
                         datetime.strptime('2017-02-14 09:30:06.610000', '%Y-%m-%d %H:%M:%S.%f'))
        self.assertEqual(transaction.action, 'BUY')
        self.assertEqual(transaction.symbol, '000001')
        self.assertEqual(transaction.price, 9.42)
        self.assertEqual(transaction.amount, 100)
