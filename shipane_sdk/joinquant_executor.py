# -*- coding: utf-8 -*-

from .client import Client


class JoinQuantExecutor(object):
    def __init__(self, **kwargs):
        self._client = Client(**kwargs)

    @property
    def client(self):
        return self._client

    @property
    def client(self):
        return self._client

    def execute(self, order):
        if order is None:
            return

        try:
            if order.is_buy:
                return self._client.buy(order.security, order.price, order.amount)
            else:
                return self._client.sell(order.security, order.price, order.amount)
        except:
            pass
