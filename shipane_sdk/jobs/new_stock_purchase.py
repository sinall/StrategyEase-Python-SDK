# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

from shipane_sdk.stock import *


class NewStockPurchaseJob(object):
    def __init__(self, config, client):
        self._log = logging.getLogger()
        self._config = config
        self._client = client

    def __call__(self):
        all_client_aliases = dict(self._config.items('ClientAliases'))
        client_aliases = self._config.get('NewStocks', 'clients').split(',')
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        df = StockUtils.new_stocks()
        df = df[(df.ipo_date == today)]
        for client_alias in client_aliases:
            client = all_client_aliases[client_alias.strip()]
            self._log.info(u'客户端[%s(%s)]开始新股申购', client_alias, client)
            for index, row in df.iterrows():
                try:
                    order = {
                        'symbol': row['xcode'], 'type': 'LIMIT', 'price': row['price'], 'amountProportion': 'ALL'
                    }
                    self._log.info(u'下单：%s', json.dumps(order))
                    response = self._client.buy(client, **order)
                    if response is not None:
                        self._log.info(u'[实盘易] 回复如下：\nstatus_code: %d\ntext: %s',
                                       response.status_code, response.text)
                    else:
                        self._log.error('[实盘易] 未回复')
                except Exception as e:
                    self._log.exception('账户[%s(%s)]申购新股[%s（%s）]失败', client_alias, client, row['name'], row['code'])
            self._log.info(u'客户端[%s(%s)]结束新股申购', client_alias, client)
