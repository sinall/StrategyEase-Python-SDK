# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import distutils
import time

from shipane_sdk.jobs.basic_job import BasicJob
from shipane_sdk.market_utils import MarketUtils
from shipane_sdk.models import AdjustmentRequest, AdjustmentContext, OrderAction, Adjustment, OrderStyle


class OnlineQuantSyncJob(BasicJob):
    def __init__(self, shipane_client, quant_client, client_aliases=None, name=None, **kwargs):
        super(OnlineQuantSyncJob, self).__init__(name, kwargs.get('schedule', None), kwargs.get('enabled', False))

        self._config = PortfolioSyncConfig(**kwargs)
        self._shipane_client = shipane_client
        self._quant_client = quant_client
        self._client_aliases = client_aliases
        self._name = name

    def __call__(self):
        if MarketUtils.is_closed() and not self._config.is_debug():
            self._logger.warning("********** 休市期间不同步 **********")
            return

        if not self._quant_client.is_login():
            self._logger.info("登录 %s", self._quant_client.name)
            self._quant_client.login()

        self._logger.info("********** 开始同步 **********")
        try:
            for client_alias in self._client_aliases:
                client = self._client_aliases[client_alias]
                self._sync(client)
        except Exception as e:
            self._logger.exception("同步异常")
        self._logger.info("********** 结束同步 **********\n")

    @property
    def name(self):
        return self._name

    def _sync(self, client):
        target_portfolio = self._get_target_portfolio()
        for i in range(0, 2 + self._config.extra_loops):
            adjustment = self._create_adjustment(target_portfolio, client)
            self._log_progress(adjustment)
            self._execute_adjustment(adjustment, client)
            time.sleep(self._config.loop_interval)

    def _get_target_portfolio(self):
        portfolio = self._quant_client.query_portfolio()
        return portfolio

    def _execute_adjustment(self, adjustment, client):
        for batch in adjustment.batches:
            for order in batch:
                self._execute_order(order, client)
                time.sleep(self._config.order_interval)
            time.sleep(self._config.batch_interval)

    def _execute_order(self, order, client):
        try:
            if self._config.is_dry_run() or self._config.is_debug():
                self._logger.info('以 %7.3f元 %s%s %5d股 %s',
                                  order.price,
                                  '限价' if order.style == OrderStyle.LIMIT else '市价',
                                  '买入' if order.action == OrderAction.OPEN else '卖出',
                                  order.amount, order.security)
                return
            action = 'BUY' if order.action == OrderAction.OPEN else 'SELL'
            self._shipane_client.execute(client=client, action=action, symbol=order.security, type='MARKET',
                                         priceType=4, amount=order.amount)
        except Exception as e:
            self._logger.error('客户端[%s]下单失败\n%s', client, e)

    def _create_adjustment(self, target_portfolio, client):
        request = self._create_adjustment_request(target_portfolio)
        request_json = AdjustmentRequest.to_json(request)
        response_json = self._shipane_client.create_adjustment(client=client, request_json=request_json)
        adjustment = Adjustment.from_json(response_json)
        return adjustment

    def _create_adjustment_request(self, target_portfolio):
        context = AdjustmentContext(self._config.reserved_securities,
                                    self._config.min_order_value,
                                    self._config.max_order_value)
        request = AdjustmentRequest(target_portfolio, context)
        return request

    def _log_progress(self, adjustment):
        self._logger.info("今日进度：[%.0f%%] ==> [%.0f%%]；总进度：[%.0f%%] ==> [%.0f%%]",
                          adjustment.today_progress.before * 100, adjustment.today_progress.after * 100,
                          adjustment.overall_progress.before * 100, adjustment.overall_progress.after * 100)


class PortfolioSyncConfig(object):
    def __init__(self, **kwargs):
        self._is_dry_run = distutils.util.strtobool(kwargs.get('dry_run', 'false'))
        self._is_debug = distutils.util.strtobool(kwargs.get('debug', 'false'))
        self._reserved_securities = [x.strip() for x in kwargs.get('reserved_securities', '').split(',')]
        self._min_order_value = kwargs.get('min_order_value', '0')
        self._max_order_value = float(kwargs.get('max_order_value', '1000000'))
        self._loop_interval = int(kwargs.get('loop_interval', '5'))
        self._batch_interval = int(kwargs.get('batch_interval', '5'))
        self._order_interval = int(kwargs.get('order_interval', '1'))
        self._extra_loops = int(kwargs.get('extra_loops', '0'))

    def is_dry_run(self):
        return self._is_dry_run

    def is_debug(self):
        return self._is_debug

    @property
    def reserved_securities(self):
        return self._reserved_securities

    @property
    def min_order_value(self):
        return self._min_order_value

    @property
    def max_order_value(self):
        return self._max_order_value

    @property
    def loop_interval(self):
        return self._loop_interval

    @property
    def batch_interval(self):
        return self._batch_interval

    @property
    def order_interval(self):
        return self._order_interval

    @property
    def extra_loops(self):
        return self._extra_loops
