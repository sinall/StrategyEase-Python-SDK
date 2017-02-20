# -*- coding: utf-8 -*-

import copy
import datetime
import re

import lxml.html
import pandas as pd
import requests
import six
from lxml import etree
from pandas.compat import StringIO
from requests import Request
from six.moves.urllib.parse import urlencode


class Client(object):
    KEY_REGEX = r'key=([^&]*)'

    def __init__(self, logger=None, **kwargs):
        self._logger = logger
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

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def get_account(self, client=None, timeout=None):
        request = Request('GET', self.__create_url(client, 'accounts'))
        response = self.__send_request(request, timeout)
        return response.json()

    def get_positions(self, client=None, timeout=None):
        request = Request('GET', self.__create_url(client, 'positions'))
        response = self.__send_request(request, timeout)
        json = response.json()
        sub_accounts = pd.DataFrame(json['subAccounts']).T
        positions = pd.DataFrame(json['dataTable']['rows'], columns=json['dataTable']['columns'])
        return {'sub_accounts': sub_accounts, 'positions': positions}

    def buy(self, client=None, timeout=None, **kwargs):
        kwargs['action'] = 'BUY'
        return self.__execute(client, timeout, **kwargs)

    def sell(self, client=None, timeout=None, **kwargs):
        kwargs['action'] = 'SELL'
        return self.__execute(client, timeout, **kwargs)

    def execute(self, client=None, timeout=None, **kwargs):
        return self.__execute(client, timeout, **kwargs)

    def cancel(self, client=None, order_id=None, timeout=None):
        request = Request('DELETE', self.__create_order_url(client, order_id))
        self.__send_request(request, timeout)

    def cancel_all(self, client=None, timeout=None):
        request = Request('DELETE', self.__create_order_url(client))
        self.__send_request(request, timeout)

    def query(self, client=None, navigation=None, timeout=None):
        request = Request('GET', self.__create_url(client, '', navigation=navigation))
        response = self.__send_request(request, timeout)
        json = response.json()
        df = pd.DataFrame(json['dataTable']['rows'], columns=json['dataTable']['columns'])
        return df

    def start_clients(self, timeout=None):
        request = Request('PUT', self.__create_url(None, 'clients'))
        self.__send_request(request, timeout)

    def shutdown_clients(self, timeout=None):
        request = Request('DELETE', self.__create_url(None, 'clients'))
        self.__send_request(request, timeout)

    def purchase_new_stocks(self, client=None):
        today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        df = self.__get_new_stocks()
        df = df[(df.ipo_date == today)]
        self._logger.info(u'今日可申购新股有%s只' % len(df))
        for index, row in df.iterrows():
            try:
                order = {
                    'symbol': row['xcode'], 'type': 'LIMIT', 'price': row['price'], 'amountProportion': 'ALL'
                }
                self._logger.info(u'申购新股：%s', str(order))
                self.buy(client, **order)
            except Exception as e:
                self._logger.exception('客户端[%s]申购新股[%s（%s）]失败', client, row['name'], row['code'])

    def __get_new_stocks(self):
        DATA_URL = 'http://vip.stock.finance.sina.com.cn/corp/view/vRPD_NewStockIssue.php?page=1&cngem=0&orderBy=NetDate&orderType=desc'
        html = lxml.html.parse(DATA_URL)
        res = html.xpath('//table[@id=\"NewStockTable\"]/tr')
        if six.PY2:
            sarr = [etree.tostring(node) for node in res]
        else:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        sarr = ''.join(sarr)
        sarr = sarr.replace('<font color="red">*</font>', '')
        sarr = '<table>%s</table>' % sarr
        df = pd.read_html(StringIO(sarr), skiprows=[0, 1])[0]
        df = df.select(lambda x: x in [0, 1, 2, 3, 7], axis=1)
        df.columns = ['code', 'xcode', 'name', 'ipo_date', 'price']
        df['code'] = df['code'].map(lambda x: str(x).zfill(6))
        df['xcode'] = df['xcode'].map(lambda x: str(x).zfill(6))
        return df

    def __execute(self, client=None, timeout=None, **kwargs):
        if not kwargs.get('type'):
            kwargs['type'] = 'LIMIT'
        request = Request('POST', self.__create_order_url(client), json=kwargs)
        response = self.__send_request(request)
        return response.json()

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

    def __send_request(self, request, timeout=None):
        prepared_request = request.prepare()
        timeout = timeout if timeout is not None else self._timeout
        self.__log_request(prepared_request)
        with requests.sessions.Session() as session:
            response = session.send(prepared_request, timeout=timeout)
        self.__log_response(response)
        response.raise_for_status()
        return response

    def __log_request(self, prepared_request):
        if self._logger is None:
            return

        url = self.__eliminate_privacy(prepared_request.path_url)
        if prepared_request.body is None:
            self._logger.info('Request:\n{} {}'.format(prepared_request.method, url))
        else:
            self._logger.info('Request:\n{} {}\n{}'.format(prepared_request.method, url, prepared_request.body))

    def __log_response(self, response):
        if self._logger is None:
            return

        message = 'Response:\n{} {}\n{}'.format(response.status_code, response.reason, response.text)
        if response.status_code == 200:
            self._logger.info(message)
        else:
            self._logger.error(message)

    @classmethod
    def __eliminate_privacy(cls, url):
        match = re.search(cls.KEY_REGEX, url)
        key = match.group(1)
        masked_key = '*' * len(key)
        url = re.sub(cls.KEY_REGEX, "key={}".format(masked_key), url)
        return url
