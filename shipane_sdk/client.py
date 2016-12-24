# -*- coding: utf-8 -*-

import copy

import requests
from six.moves.urllib.parse import urlencode


class Client(object):
    def __init__(self, **kwargs):
        self._host = kwargs.pop('host', 'localhost')
        self._port = kwargs.pop('port', 8888)
        self._key = kwargs.pop('key', '')
        self._timeout = kwargs.pop('timeout', (5.0, 10.0))

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @host.setter
    def port(self, value):
        self._port = value

    @property
    def key(self):
        return self._key

    @host.setter
    def key(self, value):
        self._key = value

    @property
    def timeout(self):
        return self._timeout

    @host.setter
    def timeout(self, value):
        self._timeout = value

    def get_account(self, client=None):
        return requests.get(self.__create_url(client, 'accounts'), timeout=self._timeout)

    def get_positions(self, client=None):
        return requests.get(self.__create_url(client, 'positions'), timeout=self._timeout)

    def buy(self, client=None, **kwargs):
        kwargs['action'] = 'BUY'
        return self.__execute(client, **kwargs)

    def sell(self, client=None, **kwargs):
        kwargs['action'] = 'SELL'
        return self.__execute(client, **kwargs)

    def execute(self, client=None, **kwargs):
        return self.__execute(client, **kwargs)

    def cancel(self, client, order_id):
        return requests.delete(self.__create_order_url(client, order_id), timeout=self._timeout)

    def cancel_all(self, client=None):
        return requests.delete(self.__create_order_url(client), timeout=self._timeout)

    def query(self, client, navigation):
        return requests.get(self.__create_url(client, '', navigation=navigation), timeout=self._timeout)

    def __execute(self, client=None, **kwargs):
        if not kwargs.get('type'):
            kwargs['type'] = 'LIMIT'
        return requests.post(self.__create_order_url(client),
                             json=kwargs,
                             timeout=self._timeout)

    def __create_order_url(self, client=None, order_id=None, **params):
        return self.__create_url(client, 'orders', order_id, **params)

    def __create_url(self, client, resource, resource_id=None, **params):
        all_params = copy.deepcopy(params)
        if client is not None:
            all_params.update(client=client)
        all_params.update(key=self._key)
        if resource_id is None:
            path = '/{}'.format(resource)
        else:
            path = '/{}/{}'.format(resource, resource_id)

        return '{}{}?{}'.format(self.__create_base_url(), path, urlencode(all_params))

    def __create_base_url(self):
        return 'http://' + self._host + ':' + str(self._port)
