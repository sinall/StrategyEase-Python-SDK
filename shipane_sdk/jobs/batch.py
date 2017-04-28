# -*- coding: utf-8 -*-

import csv
from datetime import date

from shipane_sdk.jobs.basic_job import BasicJob


class BatchJob(BasicJob):
    def __init__(self, client, client_aliases=None, name=None, **kwargs):
        super(BatchJob, self).__init__(name, kwargs.get('schedule', None), kwargs.get('enabled', False))

        self._client = client
        self._client_aliases = client_aliases
        self._folder = kwargs.get('folder')

    def __call__(self):
        file_name = '{}/{}.csv'.format(self._folder, date.today().isoformat())
        with open(file_name, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for client_alias in self._client_aliases:
                client = self._client_aliases[client_alias]
                for row in reader:
                    order = {
                        'action': 'BUY' if row[u'买卖标志'] == u'买入' else 'SELL',
                        'symbol': row[u'证券代码'],
                        'type': 'LIMIT',
                        'price': float(row[u'价格']),
                        'amount': int(row[u'数量'])
                    }
                    try:
                        self._client.execute(client, **order)
                    except Exception as e:
                        self._logger.exception("下单异常")
