# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import distutils
import time

from shipane_sdk.jobs.basic_job import BasicJob
from shipane_sdk.market_utils import MarketUtils
from shipane_sdk.models import *


class OnlineQuantSyncJob(BasicJob):
    def __init__(self, shipane_client, quant_client, client_aliases=None, name=None, **kwargs):
        super(OnlineQuantSyncJob, self).__init__(name, kwargs.get('schedule', None), kwargs.get('enabled', False))

        self._config = PortfolioSyncConfig(**kwargs)
        self._shipane_client = shipane_client
        self._quant_client = quant_client
        self._client_aliases = client_aliases
        self._name = name

    def __call__(self):
        if MarketUtils.is_closed() and not self._config.debug:
            self._logger.warning("********** 休市期间不同步 **********")
            return

        if not self._quant_client.is_login():
            self._logger.info("登录 %s", self._quant_client.name)
            self._quant_client.login()

        self._logger.info("********** 开始同步 **********")
        try:
            target_portfolio = self._get_target_portfolio()
            for client_alias in self._client_aliases:
                client = self._client_aliases[client_alias]
                self._sync(target_portfolio, client)
        except Exception as e:
            self._logger.exception("同步异常")
        self._logger.info("********** 结束同步 **********\n")

    @property
    def name(self):
        return self._name

    def _sync(self, target_portfolio, client):
        if self._config.pre_clear:
            if not self._config.debug:
                self._shipane_client.cancel_all(client)
            time.sleep(self._config.order_interval)

        for i in range(0, 2 + self._config.extra_rounds):
            is_sync = self._sync_once(target_portfolio, client)
            if is_sync:
                self._logger.info("已同步")
                return
            time.sleep(self._config.round_interval)

    def _sync_once(self, target_portfolio, client):
        adjustment = self._create_adjustment(target_portfolio, client)
        self._log_progress(adjustment)
        is_sync = adjustment.empty()
        if not is_sync:
            self._execute_adjustment(adjustment, client)
        return is_sync

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
            if self._config.debug:
                self._logger.info(order)
                return
            e_order = order.to_e_order()
            e_order['type'] = 'MARKET'
            e_order['priceType'] = 4
            self._shipane_client.execute(client=client, **e_order)
        except Exception as e:
            self._logger.error('客户端[%s]下单失败\n%s', client, e)

    def _create_adjustment(self, target_portfolio, client):
        request = self._create_adjustment_request(target_portfolio)
        request_json = Adjustment.to_json(request)
        response_json = self._shipane_client.create_adjustment(client=client, request_json=request_json)
        adjustment = Adjustment.from_json(response_json)
        return adjustment

    def _create_adjustment_request(self, target_portfolio):
        context = AdjustmentContext(self._config.reserved_securities,
                                    self._config.min_order_value,
                                    self._config.max_order_value)
        request = Adjustment()
        request.target_portfolio = target_portfolio
        request.context = context
        return request

    def _log_progress(self, adjustment):
        self._logger.info(adjustment.progress)


class PortfolioSyncConfig(object):
    def __init__(self, **kwargs):
        self._debug = distutils.util.strtobool(kwargs.get('debug', 'false'))
        self._pre_clear = distutils.util.strtobool(kwargs.get('pre_clear', 'false'))
        self._reserved_securities = list(filter(None, kwargs.get('reserved_securities').split('\n')))
        self._min_order_value = kwargs.get('min_order_value', '0')
        self._max_order_value = float(kwargs.get('max_order_value', '1000000'))
        self._round_interval = int(kwargs.get('round_interval', '5'))
        self._batch_interval = int(kwargs.get('batch_interval', '5'))
        self._order_interval = int(kwargs.get('order_interval', '1'))
        self._extra_rounds = int(kwargs.get('extra_rounds', '0'))

    @property
    def debug(self):
        return self._debug

    @property
    def pre_clear(self):
        return self._pre_clear

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
    def round_interval(self):
        return self._round_interval

    @property
    def batch_interval(self):
        return self._batch_interval

    @property
    def order_interval(self):
        return self._order_interval

    @property
    def extra_rounds(self):
        return self._extra_rounds
