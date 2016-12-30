# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from shipane_sdk.market_utils import MarketUtils


class OnlineQuantFollowingJob(object):
    def __init__(self, shipane_client, quant_client, name=None):
        self._log = logging.getLogger()
        self._shipane_client = shipane_client
        self._quant_client = quant_client
        self._name = name
        self._start_datatime = datetime.now()
        self._processed_transactions = []

    def __call__(self):
        if MarketUtils.is_closed():
            self._log.warning("********** 休市期间不跟单 **********")
            if self._processed_transactions:
                del self._processed_transactions[:]
            return

        if not self._quant_client.is_login():
            self._log.info("登录 {}".format(self._quant_client.name))
            self._quant_client.login()

        self._log.info("********** 开始跟单 **********")
        try:
            all_transactions = self._quant_client.query()
            self._log.info("获取到 {} 条委托".format(len(all_transactions)))

            transactions = []
            for transaction in all_transactions:
                if self._is_expired(transaction):
                    continue
                transactions.append(transaction)
            
            self._log.info("获取到 {} 条有效委托".format(len(transactions)))

            for tx in transactions:
                self._processed_transactions.append(tx)
                self._log.info("开始以 {}元 {} {}股 {}".format(tx.price, tx.get_cn_action(), tx.amount, tx.symbol))
                response = self._shipane_client.execute(None,
                                                        action=tx.action,
                                                        symbol=tx.symbol,
                                                        type='LIMIT',
                                                        price=tx.price,
                                                        amount=tx.amount)
                if response is not None:
                    self._log.info(u'实盘易回复：\nstatus_code: %d\ntext: %s', response.status_code, response.text)
                else:
                    self._log.error('实盘易未回复')
        except Exception as e:
            self._log.exception("跟单异常")
        self._log.info("********** 结束跟单 **********\n")

    @property
    def name(self):
        return self._name

    def _is_expired(self, transaction):
        if transaction.completed_at < self._start_datatime:
            return True
        if transaction in self._processed_transactions:
            return True
        return False
