# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from shipane_sdk.stock import *


class NewStockPurchaseJob(object):
    def __init__(self, config, client, client_aliases=None):
        self._logger = logging.getLogger()
        self._config = config
        self._client = client
        self._client_aliases = client_aliases

    def __call__(self):
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        df = StockUtils.new_stocks()
        df = df[(df.ipo_date == today)]
        for client_alias in self._client_aliases:
            client = self._client_aliases[client_alias]
            self._logger.info(u'客户端[%s(%s)]开始新股申购', client_alias, client)
            for index, row in df.iterrows():
                try:
                    order = {
                        'symbol': row['xcode'], 'type': 'LIMIT', 'price': row['price'], 'amountProportion': 'ALL'
                    }
                    self._logger.info(u'下单：%s', json.dumps(order))
                    self._client.buy(client, **order)
                except Exception as e:
                    self._logger.exception('账户[%s(%s)]申购新股[%s（%s）]失败', client_alias, client, row['name'], row['code'])
            self._logger.info(u'客户端[%s(%s)]结束新股申购', client_alias, client)
