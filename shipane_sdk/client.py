# -*- coding: utf-8 -*-

import copy

import requests
from requests import Request
from six.moves.urllib.parse import urlencode


class Client(object):
    def __init__(self, log=None, **kwargs):
        self._log = log
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
        request = Request('GET', self.__create_url(client, 'accounts'))
        response = self.__send_request(request)
        return response

    def get_positions(self, client=None):
        request = Request('GET', self.__create_url(client, 'positions'))
        response = self.__send_request(request)
        return response

    def buy(self, client=None, **kwargs):
        kwargs['action'] = 'BUY'
        return self.__execute(client, **kwargs)

    def sell(self, client=None, **kwargs):
        kwargs['action'] = 'SELL'
        return self.__execute(client, **kwargs)

    def execute(self, client=None, **kwargs):
        return self.__execute(client, **kwargs)

    def cancel(self, client, order_id):
        request = Request('DELETE', self.__create_order_url(client, order_id))
        response = self.__send_request(request)
        return response

    def cancel_all(self, client=None):
        request = Request('DELETE', self.__create_order_url(client))
        response = self.__send_request(request)
        return response

    def query(self, client, navigation):
        request = Request('GET', self.__create_url(client, '', navigation=navigation))
        response = self.__send_request(request)
        return response

    def __execute(self, client=None, **kwargs):
        if not kwargs.get('type'):
            kwargs['type'] = 'LIMIT'
        request = Request('POST', self.__create_order_url(client), json=kwargs)
        response = self.__send_request(request)
        return response

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

    def __send_request(self, request):
        prepared_request = request.prepare()
        self.__log_request(request)
        with requests.sessions.Session() as session:
            response = session.send(prepared_request, timeout=self._timeout)
        self.__log_response(response)
        return response

    def __log_request(self, request):
        if self._log is None:
            return

        if request.json is None:
            self._log.info('Request:\n%s %s', request.method, request.url)
        else:
            self._log.info('Request:\n%s %s\n%s', request.method, request.url, request.json)

    def __log_response(self, response):
        if self._log is None:
            return

        message = 'Response:\n{} {}\n{}'.format(response.status_code, response.reason, response.text)
        if response.status_code == 200:
            self._log.info(message)
        else:
            self._log.error(message)
