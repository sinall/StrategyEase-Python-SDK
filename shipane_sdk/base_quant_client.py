# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime


class BaseQuantClient(object):
    def __init__(self, name):
        self._name = name
        self._last_login_time = datetime.now() - timedelta(1)

    @property
    def name(self):
        return self._name

    def login(self):
        self._last_login_time = datetime.now()

    def is_login(self):
        return self._last_login_time >= datetime.combine(date.today(), datetime.min.time())

    def query(self):
        return []
