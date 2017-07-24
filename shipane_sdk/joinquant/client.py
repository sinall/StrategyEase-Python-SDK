# -*- coding: utf-8 -*-

from datetime import datetime

import requests
from bs4 import BeautifulSoup

from shipane_sdk.base_quant_client import BaseQuantClient
from shipane_sdk.joinquant.transaction import JoinQuantTransaction
from shipane_sdk.models import Portfolio, Position


class JoinQuantClient(BaseQuantClient):
    BASE_URL = 'https://www.joinquant.com'

    def __init__(self, **kwargs):
        super(JoinQuantClient, self).__init__('JoinQuant')

        self._session = requests.Session()
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)
        self._backtest_id = kwargs.get('backtest_id', None)
        self._arena_id = kwargs.get('arena_id', None)
        self._timeout = kwargs.pop('timeout', (5.0, 10.0))

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
        self._session.get(self.BASE_URL, timeout=self._timeout)
        response = self._session.post('{}/user/login/doLogin?ajax=1'.format(self.BASE_URL), data={
            'CyLoginForm[username]': self._username,
            'CyLoginForm[pwd]': self._password,
            'ajax': 1
        }, timeout=self._timeout)
        self._session.headers.update({
            'cookie': response.headers['Set-Cookie']
        })

        super(JoinQuantClient, self).login()

    def query(self):
        today_str = datetime.today().strftime('%Y-%m-%d')
        response = self._session.get('{}/algorithm/live/transactionDetail'.format(self.BASE_URL), params={
            'backtestId': self._backtest_id,
            'date': today_str,
            'ajax': 1
        }, timeout=self._timeout)
        transaction_detail = response.json()
        raw_transactions = transaction_detail['data']['transaction']
        transactions = []
        for raw_transaction in raw_transactions:
            transaction = JoinQuantTransaction(raw_transaction).normalize()
            transactions.append(transaction)

        return transactions

    def query_portfolio(self):
        today_str = datetime.today().strftime('%Y-%m-%d')
        strategy_res = self._session.get('{}/post/{}'.format(self.BASE_URL, self._arena_id))
        strategy_soup = BeautifulSoup(strategy_res.content, "lxml")
        backtest_id = strategy_soup.findAll('input', id="backtestId").pop().get('value')
        total_value = float(strategy_soup.findAll('div', class_="inline-block num f18 red").pop().text)
        position_res = self._session.get('{}/algorithm/live/sharePosition'.format(self.BASE_URL), params={
            'isAjax': 1,
            'backtestId': backtest_id,
            'date': today_str,
            'isMobile': 0,
            'isForward': 1,
            'ajax': 1})
        position_soup = BeautifulSoup(position_res.json()['data']['html'], "lxml")
        trs = position_soup.findAll('tr', class_="border_bo position_tr")
        positions = dict()
        positions_value = 0
        for tr in trs:
            position = self.__tr_to_position(tr)
            positions_value += position.value
            positions[position.security] = position
        portfolio = Portfolio()
        portfolio.total_value = total_value
        portfolio.available_cash = total_value - positions_value
        portfolio.positions = positions
        return portfolio

    def __tr_to_position(self, tr):
        tds = tr.findAll('td')
        position = Position()
        position.security = tds[0].text.split()[1]
        position.price = float(tds[7].text)
        position.total_amount = int(tds[2].text.replace(u'股', ''))
        position.value = float(tds[4].text)
        return position
