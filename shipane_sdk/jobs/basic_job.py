# -*- coding: utf-8 -*-

import logging


class BasicJob(object):
    def __init__(self, name=None, schedule=None, is_enabled=False):
        self._logger = logging.getLogger()
        self._name = name
        self._schedule = schedule
        self._is_enabled = is_enabled

    def __call__(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def schedule(self):
        return self._schedule

    @property
    def is_enabled(self):
        return self._is_enabled
