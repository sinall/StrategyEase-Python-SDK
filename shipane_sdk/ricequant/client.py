# -*- coding: utf-8 -*-

from rqopen_client import RQOpenClient


class RiceQuantClient(object):
    def __init__(self, **kwargs):
        self._run_id = kwargs.pop('run_id')
        self._rq_client = RQOpenClient(kwargs.pop('username'), kwargs.pop('password'))

    def login(self):
        self._rq_client.login()

    def query(self):
        return self._rq_client.get_day_trades(self._run_id)
