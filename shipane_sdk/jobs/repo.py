# -*- coding: utf-8 -*-

import tushare as ts

from shipane_sdk.jobs.basic_job import BasicJob


class RepoJob(BasicJob):
    def __init__(self, client, client_aliases=None, name=None, **kwargs):
        super(RepoJob, self).__init__(name, kwargs.get('schedule', None), kwargs.get('enabled', False))

        self._client = client
        self._client_aliases = client_aliases
        self._symbol = kwargs.get('security', '131810')

    def __call__(self):
        df = ts.get_realtime_quotes(self._symbol)
        order = {
            'action': 'SELL',
            'symbol': self._symbol,
            'type': 'LIMIT',
            'price': float(df['bid'][0]),
            'amountProportion': 'ALL'
        }
        for client_alias in self._client_aliases:
            try:
                client = self._client_aliases[client_alias]
                self._client.execute(client, **order)
            except:
                self._logger.exception('客户端[%s]逆回购失败', client_alias)
