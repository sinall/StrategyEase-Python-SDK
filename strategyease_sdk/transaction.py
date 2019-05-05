# -*- coding: utf-8 -*-


class Transaction(object):
    def __init__(self, **kwargs):
        self._completed_at = kwargs.get('completed_at')
        self._action = kwargs.get('action')
        self._symbol = kwargs.get('symbol')
        self._price = kwargs.get('price')
        self._amount = kwargs.get('amount')

    def __eq__(self, other):
        if self.completed_at != other.completed_at:
            return False
        if self.action != other.action:
            return False
        if self.symbol != other.symbol:
            return False
        if self.price != other.price:
            return False
        if self.amount != other.amount:
            return False
        return True

    def get_cn_action(self):
        return u'买入' if self.action == 'BUY' else u'卖出'

    @property
    def completed_at(self):
        return self._completed_at

    @completed_at.setter
    def completed_at(self, value):
        self._completed_at = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
