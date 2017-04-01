# -*- coding: utf-8 -*-

from rqopen_client import RQOpenClient

from shipane_sdk.base_quant_client import BaseQuantClient
from shipane_sdk.ricequant.transaction import RiceQuantTransaction


class RiceQuantClient(BaseQuantClient):
    def __init__(self, **kwargs):
        super(RiceQuantClient, self).__init__('RiceQuant')

        self._rq_client = RQOpenClient(kwargs.get('username', None), kwargs.get('password', None),
                                       timeout=kwargs.pop('timeout', (5.0, 10.0)))
        self._run_id = kwargs.get('run_id', None)

    def login(self):
        self._rq_client.login(timeout=self._timeout)
        super(RiceQuantClient, self).login()

    def query(self):
        response = self._rq_client.get_day_trades(self._run_id, timeout=self._timeout)
        raw_transactions = response['resp']['trades']
        transactions = []
        for raw_transaction in raw_transactions:
            transaction = RiceQuantTransaction(raw_transaction).normalize()
            transactions.append(transaction)

        return transactions
