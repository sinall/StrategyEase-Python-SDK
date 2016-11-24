# -*- coding: utf-8 -*-

from .client import Client


#
# 聚宽整合请从这里开始拷贝
#
class JoinQuantExecutor(object):
    def __init__(self, **kwargs):
        self._client = Client(**kwargs)
        self.order_id_map = dict()

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
                response = self._client.buy(order.security, order.price, order.amount)
            else:
                response = self._client.sell(order.security, order.price, order.amount)

            if response is None:
                return None

            if response.status_code == 200:
                self.order_id_map[order.order_id] = response.json()['id'];

            return response
        except:
            pass

    def cancel(self, order):
        if order is None:
            return

        try:
            order_id = order if isinstance(order, int) else order.order_id
            if order_id in self.order_id_map:
                return self._client.cancel(self.order_id_map[order_id])
            else:
                pass
        except:
            pass
