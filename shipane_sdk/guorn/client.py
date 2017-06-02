# -*- coding: utf-8 -*-

import time

import pandas as pd
import requests

from shipane_sdk.base_quant_client import BaseQuantClient
from shipane_sdk.models import *


class GuornClient(BaseQuantClient):
    BASE_URL = 'https://guorn.com'

    def __init__(self, **kwargs):
        super(GuornClient, self).__init__('Guorn')

        self._session = requests.Session()
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)
        self._sid = kwargs.get('sid', None)
        self._timeout = kwargs.pop('timeout', (5.0, 10.0))

    def login(self):
        self._session.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Referer': '{}'.format(self.BASE_URL),
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.BASE_URL,
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self._session.get(self.BASE_URL, timeout=self._timeout)
        response = self._session.post('{}/user/login'.format(self.BASE_URL), json={
            'account': self._username,
            'passwd': self._password,
            'keep_login': 'true'
        }, timeout=self._timeout)
        self._session.headers.update({
            'cookie': response.headers['Set-Cookie']
        })

        super(GuornClient, self).login()

    def query_portfolio(self):
        response = self._session.get('{}/stock/instruction'.format(self.BASE_URL), params={
            'fmt': 'json',
            'amount': 1000000,
            'sid': self._sid,
            '_': time.time()
        }, timeout=self._timeout)
        instruction = response.json()

        data = instruction['data']
        position = data['position']
        df = pd.DataFrame()
        sheet_data = instruction['data']['sheet_data']
        for row in sheet_data['row']:
            df[row['name']] = pd.Series(row['data'][1])
        meas_data = sheet_data['meas_data']
        for index, col in enumerate(sheet_data['col']):
            df[col['name']] = pd.Series(meas_data[index])

        portfolio = Portfolio(total_value=1.0)
        for index, row in df.iterrows():
            security = row[u'股票代码']
            value = row[u'目标仓位']
            price = row[u'参考价']
            amount = value / price
            position = Position(security, price, amount, amount)
            portfolio.add_position(position)
        portfolio.rebalance()

        return portfolio
