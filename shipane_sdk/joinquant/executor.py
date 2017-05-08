# -*- coding: utf-8 -*-

import datetime

from shipane_sdk.client import Client

try:
    from kuanke.user_space_api import *
except:
    pass


class JoinQuantExecutor(object):
    def __init__(self, **kwargs):
        try:
            log
            self._logger = _Logger()
        except NameError:
            import logging
            self._logger = logging.getLogger()
        self._client = Client(self._logger, **kwargs)
        self._client_param = kwargs.get('client')
        self._order_id_map = dict()
        self._expire_before = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    @property
    def client(self):
        return self._client

    def purchase_new_stocks(self):
        self.client.purchase_new_stocks(self._client_param)

    def execute(self, order):
        self._logger.info("[实盘易] 跟单：" + str(order))

        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略下单请求')
            return
        if self.__is_expired(order):
            self._logger.info('[实盘易] 委托已过期，忽略下单请求')
            return

        try:
            action = 'BUY' if order.is_buy else 'SELL'
            order_type = 'LIMIT' if order.limit > 0 else 'MARKET'
            price_type = 0 if order_type == 'LIMIT' else 4
            actual_order = self._client.execute(self._client_param,
                                                action=action,
                                                symbol=order.security,
                                                type=order_type,
                                                priceType=price_type,
                                                price=order.limit,
                                                amount=order.amount)
            self._order_id_map[order.order_id] = actual_order['id']
            return actual_order
        except Exception as e:
            self._logger.error("[实盘易] 下单异常：" + str(e))

    def cancel(self, order):
        if order is None:
            self._logger.info('[实盘易] 委托为空，忽略撤单请求')
            return

        try:
            order_id = order if isinstance(order, int) else order.order_id
            if order_id in self._order_id_map:
                self._client.cancel(self._client_param, self._order_id_map[order_id])
            else:
                self._logger.warning('[实盘易] 未找到对应的委托编号')
        except Exception as e:
            self._logger.error("[实盘易] 撤单异常：" + str(e))

    def __is_expired(self, order):
        return order.add_time < self._expire_before


class _Logger(object):
    def debug(self, msg, *args, **kwargs):
        log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        log.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        log.error(msg, *args, **kwargs)
