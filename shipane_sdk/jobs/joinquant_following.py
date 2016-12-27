# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from shipane_sdk.joinquant.client import JoinQuantClient
from shipane_sdk.joinquant.transaction import JoinQuantTransaction
from shipane_sdk.market_utils import MarketUtils


class JoinQuantFollowingJob(object):
    def __init__(self, config, client):
        self._log = logging.getLogger()
        self._config = config
        self._client = client
        self._jq_client = JoinQuantClient(username=self._config.get('JoinQuant', 'username'),
                                          password=self._config.get('JoinQuant', 'password'),
                                          backtest_id=self._config.get('JoinQuant', 'backtest_id'))
        self._jq_client.login()
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
            transaction_detail = self._jq_client.query()
            raw_transactions = transaction_detail['data']['transaction']
            self._log.info("获取到 {} 条委托".format(len(raw_transactions)))

            transactions = []
            for raw_transaction in raw_transactions:
                transaction = JoinQuantTransaction(raw_transaction).normalize()
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
