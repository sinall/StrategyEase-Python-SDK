# -*- coding: utf-8 -*-

import re
from datetime import datetime

from shipane_sdk.transaction import Transaction


class JoinQuantTransaction(object):
    def __init__(self, json):
        self.__dict__.update(json)

    def normalize(self):
        transaction = Transaction()
        transaction.completed_at = datetime.strptime('{} {}'.format(self.date, self.time), '%Y-%m-%d %H:%M')
        transaction.action = 'BUY' if self.transaction == u'买' else 'SELL'
        transaction.symbol = re.search(".*\\((\\d+)\\..*\\)", self.stock).group(1)
        transaction.price = self.price
        transaction.amount = int(re.search(u".*>[-]*(\\d+).*", self.amount, re.UNICODE).group(1))
        return transaction
