# -*- coding: utf-8 -*-

# Begin of __future__ module
# End   of __future__ module

# Begin of external module
# End   of external module

import datetime

from shipane_sdk.client import Client


class RiceQuantExecutor(object):
    def __init__(self, **kwargs):
        self._logger = self._create_logger()
        self._shipane_client = Client(self._logger, **kwargs)
        self._order_id_map = dict()
        self._expire_before = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    @property
    def client(self):
        return self._shipane_client

    def purchase_new_stocks(self):
        self.client.purchase_new_stocks()

    def execute(self, order):
        self._logger.info("[实盘易] 跟单：{}".format(order))

        if not self._should_execute(order):
            return

        try:
            e_order = self._convert_order(order)
            actual_order = self._shipane_client.execute(**e_order)
            self._order_id_map[order.order_id] = actual_order['id']
            return actual_order
        except Exception as e:
            self._logger.error("[实盘易] 下单异常：{}".format(e))

    def cancel(self, order_id):
        if order_id is None:
            self._logger.info('[实盘易] 委托为空，忽略撤单请求')
            return

        try:
            if order_id in self._order_id_map:
                self._shipane_client.cancel(order_id=self._order_id_map[order_id])
            else:
                self._logger.warning('[实盘易] 未找到对应的委托编号')
        except Exception as e:
            self._logger.error("[实盘易] 撤单异常：{}".format(e))

    def _create_logger(self):
        try:
            return logger
        except NameError:
            import logging
            return logging.getLogger()

    def _should_execute(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略下单请求')
            return False
        if self._is_expired(order):
            self._logger.info('[实盘易] 委托已过期，忽略下单请求')
            return False
        return True

    def _is_expired(self, order):
        return order.datetime < self._expire_before

    def _convert_order(self, order):
        price_type = 0 if order.type.name == 'LIMIT' else 4
        e_order = dict(
            action=order.side.name,
            symbol=order.order_book_id,
            type=order.type.name,
            priceType=price_type,
            price=order.price,
            amount=order.quantity
        )
        return e_order
