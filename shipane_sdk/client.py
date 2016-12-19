# -*- coding: utf-8 -*-

import copy

import requests
from six.moves.urllib.parse import urlencode


class Client(object):
    def __init__(self, **kwargs):
        self._host = kwargs.pop('host', 'localhost')
        self._port = kwargs.pop('port', 8888)
        self._key = kwargs.pop('key', '')
        self._title = kwargs.pop('title', 'monijiaoyi')
        self._account = kwargs.pop('account', '')
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
    def title(self):
        return self._title

    @host.setter
    def title(self, value):
        self._title = value

    @property
    def account(self):
        return self._account

    @host.setter
    def account(self, value):
        self._account = value

    @property
    def timeout(self):
        return self._timeout

    @host.setter
    def timeout(self, value):
        self._timeout = value

    def get_account(self):
        return requests.get(self.__create_url('accounts'), timeout=self._timeout)

    def get_positions(self):
        return requests.get(self.__create_url('positions'), timeout=self._timeout)

    def buy(self, symbol, price, amount):
        return self.__execute('BUY', symbol, price, amount)

    def sell(self, symbol, price, amount):
        return self.__execute('SELL', symbol, price, amount)

    def execute(self, action, symbol, price, amount):
        return self.__execute(action, symbol, price, amount)

    def cancel(self, order_id):
        return requests.delete(self.__create_order_url(order_id), timeout=self._timeout)

    def cancel_all(self):
        return requests.delete(self.__create_order_url(), timeout=self._timeout)

    def query(self, navigation):
        return requests.get(self.__create_url('', navigation=navigation), timeout=self._timeout)

    def __execute(self, action, symbol, price, amount):
        return requests.post(self.__create_order_url(),
                             json={'action': action, 'symbol': symbol, 'type': 'LIMIT', 'price': price, 'amount': amount},
                             timeout=self._timeout)

    def __create_order_url(self, order_id=None, **params):
        return self.__create_url('orders', order_id, **params)

    def __create_url(self, resource, resource_id=None, **params):
        client_param = self.__create_client_param()
        all_params = copy.deepcopy(params)
        all_params.update(client=client_param, key=self._key)
        if resource_id is None:
            path = '/{}'.format(resource)
        else:
            path = '/{}/{}'.format(resource, resource_id)

        return '{}{}?{}'.format(self.__create_base_url(), path, urlencode(all_params))

    def __create_base_url(self):
        return 'http://' + self._host + ':' + str(self._port)

    def __create_client_param(self):
        client_param = ''
        if self._title:
            client_param += 'title:' + self._title
        if self._account:
            if client_param:
                client_param += ','
            client_param += 'account:' + self._account
        return client_param
