# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from shipane_sdk.market_utils import MarketUtils
from shipane_sdk.ricequant.client import RiceQuantClient
from shipane_sdk.ricequant.transaction import RiceQuantTransaction


class RiceQuantFollowingJob(object):
    def __init__(self, config, client):
        self._log = logging.getLogger()
        self._config = config
        self._client = client
        self._rq_client = RiceQuantClient(username=self._config.get('RiceQuant', 'username'),
                                          password=self._config.get('RiceQuant', 'password'),
                                          run_id=self._config.get('RiceQuant', 'run_id'))
        self._rq_client.login()
        self._start_datatime = datetime.now()
        self._processed_transactions = []

    def __call__(self):
        if MarketUtils.is_closed():
            self._log.warning("********** 休市期间不跟单 **********")
            if self._processed_transactions:
                del self._processed_transactions[:]
            return

        self._log.info("********** 开始跟单 **********")
        try:
            transaction_detail = self._rq_client.query()
            raw_transactions = transaction_detail['resp']['trades']
            self._log.info("获取到 {} 条委托".format(len(raw_transactions)))

            transactions = []
            for raw_transaction in raw_transactions:
                transaction = RiceQuantTransaction(raw_transaction).normalize()
                if self._is_expired(transaction):
                    continue

                transactions.append(transaction)
            self._log.info("获取到 {} 条有效委托".format(len(transactions)))

            for tx in transactions:
                self._processed_transactions.append(tx)
                self._log.info("开始以 {}元 {} {}股 {}".format(tx.price, tx.get_cn_type(), tx.amount, tx.symbol))
                response = self._shipane_client.execute(None,
                                                        action=tx.type,
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

    def _is_expired(self, transaction):
        if transaction.completed_at < self._start_datatime:
            return True
        if transaction in self._processed_transactions:
            return True
        return False
