# -*- coding: utf-8 -*-

from datetime import datetime

from shipane_sdk.transaction import Transaction


class UqerTransaction(object):
    def __init__(self, json):
        self.__dict__.update(json)

    def normalize(self):
        transaction = Transaction()
        transaction.completed_at = datetime.fromtimestamp(self.place_time / 1000.0)
        transaction.action = self.side
        transaction.symbol = self.ticker
        transaction.price = self.execution_avg_price
        transaction.amount = abs(self.amount)
        return transaction
