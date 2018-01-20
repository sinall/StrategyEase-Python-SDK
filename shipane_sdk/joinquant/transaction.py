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
        transaction.type = 'LIMIT' if self.type == u'限价单' else 'MARKET'
        if transaction.type == 'LIMIT':
            transaction.priceType = 0
            transaction.price = self.limitPrice
        else:
            transaction.priceType = 4
            transaction.price = self.price
        transaction.amount = int(re.search(u".*>[-]*(\\d+).*", self.orderAmount, re.UNICODE).group(1))
        return transaction
