# -*- coding: utf-8 -*-

from datetime import datetime

from shipane_sdk.transaction import Transaction


class RiceQuantTransaction(object):
    def __init__(self, json):
        self.__dict__.update(json)

    def normalize(self):
        transaction = Transaction()
        transaction.completed_at = datetime.strptime(self.time, '%Y-%m-%d %H:%M:%S')
        transaction.action = 'BUY' if self.quantity > 0 else 'SELL'
        transaction.symbol = self.order_book_id
        transaction.price = self.price
        transaction.amount = abs(self.quantity)
        return transaction
