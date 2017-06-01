# -*- coding: utf-8 -*-

from datetime import datetime

from requests import HTTPError

from shipane_sdk.jobs.basic_job import BasicJob
from shipane_sdk.market_utils import MarketUtils


class OnlineQuantFollowingJob(BasicJob):
    def __init__(self, shipane_client, quant_client, client_aliases=None, name=None, **kwargs):
        super(OnlineQuantFollowingJob, self).__init__(name, kwargs.get('schedule', None), kwargs.get('enabled', False))

        self._shipane_client = shipane_client
        self._quant_client = quant_client
        self._client_aliases = client_aliases
        self._name = name
        self._start_datatime = datetime.now()
        self._processed_transactions = []

    def __call__(self):
        if MarketUtils.is_closed():
            self._logger.warning("********** 休市期间不跟单 **********")
            if self._processed_transactions:
                del self._processed_transactions[:]
            return

        if not self._quant_client.is_login():
            self._logger.info("登录 %s", self._quant_client.name)
            self._quant_client.login()

        self._logger.info("********** 开始跟单 **********")
        try:
            all_transactions = self._quant_client.query()
            self._logger.info("获取到 %d 条委托", len(all_transactions))

            transactions = []
            for transaction in all_transactions:
                if self._is_expired(transaction):
                    continue
                transactions.append(transaction)
            self._logger.info("获取到 %d 条有效委托", len(transactions))

            for client_alias in self._client_aliases:
                client = self._client_aliases[client_alias]
                for tx in transactions:
                    try:
                        self._processed_transactions.append(tx)
                        self._logger.info("开始在[%s(%s)]以 %f元 %s %d股 %s",
                                          client_alias, client, tx.price, tx.get_cn_action(), tx.amount, tx.symbol)
                        self._shipane_client.execute(client,
                                                     action=tx.action,
                                                     symbol=tx.symbol,
                                                     type=tx.type,
                                                     priceType=tx.priceType,
                                                     price=tx.price,
                                                     amount=tx.amount)
                    except HTTPError as e:
                        self._logger.exception("下单异常")
        except Exception as e:
            self._logger.exception("跟单异常")
        self._logger.info("********** 结束跟单 **********\n")

    @property
    def name(self):
        return self._name

    def _is_expired(self, transaction):
        if transaction.completed_at < self._start_datatime:
            return True
        if transaction in self._processed_transactions:
            return True
        return False
