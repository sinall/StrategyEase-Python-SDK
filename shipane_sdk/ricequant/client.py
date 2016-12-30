# -*- coding: utf-8 -*-

from rqopen_client import RQOpenClient

from shipane_sdk.base_quant_client import BaseQuantClient
from shipane_sdk.ricequant.transaction import RiceQuantTransaction


class RiceQuantClient(BaseQuantClient):
    def __init__(self, **kwargs):
        super(RiceQuantClient, self).__init__('RiceQuant')

        self._run_id = kwargs.pop('run_id')
        self._rq_client = RQOpenClient(kwargs.pop('username'), kwargs.pop('password'))

    def login(self):
        self._rq_client.login()
        super(RiceQuantClient, self).login()

    def query(self):
        response = self._rq_client.get_day_trades(self._run_id)
        raw_transactions = response['resp']['trades']
        transactions = []
        for raw_transaction in raw_transactions:
            transaction = RiceQuantTransaction(raw_transaction).normalize()
            transactions.append(transaction)

        return transactions
