# -*- coding: utf-8 -*-

from shipane_sdk.jobs.basic_job import BasicJob


class ConvertibleBondsPurchaseJob(BasicJob):
    def __init__(self, client, client_aliases=None, name=None, **kwargs):
        super(ConvertibleBondsPurchaseJob, self).__init__(name, kwargs.get('schedule', None), kwargs.get('enabled', False))

        self._client = client
        self._client_aliases = client_aliases

    def __call__(self):
        for client_alias in self._client_aliases:
            try:
                client = self._client_aliases[client_alias]
                self._client.purchase_convertible_bonds(client)
            except:
                self._logger.exception('客户端[%s]申购转债失败', client_alias)
