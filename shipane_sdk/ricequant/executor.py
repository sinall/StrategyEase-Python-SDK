# -*- coding: utf-8 -*-

import datetime

try:
    from shipane_sdk.client import Client
except:
    pass


class RiceQuantExecutor(object):
    def __init__(self, **kwargs):
        try:
            self._logger = logger
        except NameError:
            import logging
            self._logger = logging.getLogger()
        self._client = Client(self._logger, **kwargs)
        self._client_param = kwargs.get('client')
        self._order_id_map = dict()
        self._started_at = datetime.datetime.now()

    @property
    def client(self):
        return self._client

    @property
    def client(self):
        return self._client

    def execute(self, order_id):
        if order_id is None:
            self._logger.info('[实盘易] 委托为空，忽略下单请求')
            return

        try:
            order = get_order(order_id)
            if order is None:
                self._logger.info('[实盘易] 委托为空，忽略下单请求')
                return

            if self.__is_expired(order):
                self._logger.info('[实盘易] 委托已过期，忽略下单请求')
                return

            price_type = 0 if order.type.name == 'LIMIT' else 4
            actual_order = self._client.execute(self._client_param,
                                                action=order.side.name,
                                                symbol=order.order_book_id,
                                                type=order.type.name,
                                                priceType=price_type,
                                                price=order.price,
                                                amount=order.quantity)
            self._order_id_map[order_id] = actual_order['id']
            return actual_order
        except Exception as e:
            self._logger.error("[实盘易] 下单异常：" + str(e))

    def cancel(self, order_id):
        if order_id is None:
            self._logger.info('[实盘易] 委托为空，忽略撤单请求')
            return

        try:
            if order_id in self._order_id_map:
                self._client.cancel(self._client_param, self._order_id_map[order_id])
            else:
                self._logger.warning('[实盘易] 未找到对应的委托编号')
        except Exception as e:
            self._logger.error("[实盘易] 撤单异常：" + str(e))

    def __is_expired(self, order):
        return order.datetime < self._started_at
