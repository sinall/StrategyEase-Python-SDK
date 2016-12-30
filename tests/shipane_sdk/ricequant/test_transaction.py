# -*- coding: utf-8 -*-
import json
import os
import unittest
from datetime import datetime

from shipane_sdk.ricequant.transaction import RiceQuantTransaction


class TransactionTest(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open('{}/../../sample_data/rq_client-response.json'.format(dir_path)) as data_file:
            self._transaction_detail = json.loads(data_file.read())

    def test_from_raw(self):
        rq_transaction = RiceQuantTransaction(self._transaction_detail['resp']['trades'][0])
        transaction = rq_transaction.normalize()
        self.assertEqual(transaction.completed_at, datetime.strptime('2016-12-23 09:32:00', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(transaction.action, 'SELL')
        self.assertEqual(transaction.symbol, '600216.XSHG')
        self.assertEqual(transaction.price, 12.77)
        self.assertEqual(transaction.amount, 100)
