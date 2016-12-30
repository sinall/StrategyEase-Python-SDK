# -*- coding: utf-8 -*-

from datetime import datetime

import requests

from shipane_sdk.base_quant_client import BaseQuantClient
from shipane_sdk.joinquant.transaction import JoinQuantTransaction


class JoinQuantClient(BaseQuantClient):
    BASE_URL = 'https://www.joinquant.com'

    def __init__(self, **kwargs):
        super(JoinQuantClient, self).__init__('JoinQuant')

        self._session = requests.Session()
        self._username = kwargs.pop('username')
        self._password = kwargs.pop('password')
        self._backtest_id = kwargs.pop('backtest_id')

    def login(self):
        self._session.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Referer': '{}/user/login/index'.format(self.BASE_URL),
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.BASE_URL,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self._session.get(self.BASE_URL)
        response = self._session.post('{}/user/login/doLogin?ajax=1'.format(self.BASE_URL), data={
            'CyLoginForm[username]': self._username,
            'CyLoginForm[pwd]': self._password,
            'ajax': 1
        })
        self._session.headers.update({
            'cookie': response.headers['Set-Cookie']
        })

        super(JoinQuantClient, self).login()

    def query(self):
        today_str = datetime.today().strftime('%Y-%m-%d')
        response = self._session.get('{}/algorithm/live/transactionDetail'.format(self.BASE_URL), params={
            'backtestId': self._backtest_id,
            'data': today_str,
            'ajax': 1
        })
        transaction_detail = response.json()
        raw_transactions = transaction_detail['data']['transaction']
        transactions = []
        for raw_transaction in raw_transactions:
            transaction = JoinQuantTransaction(raw_transaction).normalize()
            transactions.append(transaction)

        return transactions
