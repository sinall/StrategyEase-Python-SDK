# -*- coding: utf-8 -*-

try:
    from shipane_sdk.client import Client
except:
    pass

try:
    from kuanke.user_space_api import *
except:
    pass


class JoinQuantExecutor(object):
    def __init__(self, **kwargs):
        if 'log' in globals():
            self._log = log
        else:
            import logging
            self._log = logging.getLogger()
        self._client = Client(**kwargs)
        self._client_param = kwargs.get('client')
        self._order_id_map = dict()

    @property
    def client(self):
        return self._client

    @property
    def client(self):
        return self._client

    def execute(self, order):
        if order is None:
            self._log.info('[实盘易] 委托为空，忽略下单请求')
            return

        try:
            action = 'BUY' if order.is_buy else 'SELL'
            response = self._client.execute(self._client_param,
                                            action=action,
                                            symbol=order.security,
                                            price=order.price,
                                            amount=order.amount)

            if response is not None:
                self._log.info(u'[实盘易] 回复如下：\nstatus_code: %d\ntext: %s', response.status_code, response.text)
            else:
                self._log.error('[实盘易] 未回复')

            if response is None:
                return None

            if response.status_code == 200:
                self._order_id_map[order.order_id] = response.json()['id'];

            return response
        except Exception as e:
            self._log.error("[实盘易] 下单异常：" + str(e))

    def cancel(self, order):
        if order is None:
            self._log.info('[实盘易] 委托为空，忽略撤单请求')
            return

        try:
            order_id = order if isinstance(order, int) else order.order_id
            if order_id in self._order_id_map:
                return self._client.cancel(self._client_param, self._order_id_map[order_id])
            else:
                self._log.warn('[实盘易] 未找到对应的委托编号')
        except Exception as e:
            self._log.error("[实盘易] 撤单异常：" + str(e))
