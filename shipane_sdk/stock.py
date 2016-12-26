# -*- coding: utf-8 -*-

import lxml.html.soupparser
import pandas as pd
import requests


class StockUtils(object):
    @staticmethod
    def new_stocks():
        url = 'http://vip.stock.finance.sina.com.cn/corp/view/vRPD_NewStockIssue.php?page=1&cngem=0&orderBy=NetDate&orderType=desc'
        request = requests.get(url)
        doc = lxml.html.soupparser.fromstring(request.content, features='html.parser')
        table = doc.cssselect('table#NewStockTable')[0]
        table.remove(table.cssselect('thead')[0])
        table_html = lxml.html.etree.tostring(table).decode('utf-8')
        df = pd.read_html(table_html, skiprows=[0, 1])[0]
        df = df.select(lambda x: x in [0, 1, 2, 3, 7], axis=1)
        df.columns = ['code', 'xcode', 'name', 'ipo_date', 'price']
        df['code'] = df['code'].map(lambda x: str(x).zfill(6))
        df['xcode'] = df['xcode'].map(lambda x: str(x).zfill(6))
        return df
