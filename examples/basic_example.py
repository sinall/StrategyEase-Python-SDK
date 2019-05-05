# -*- coding: utf-8 -*-

import logging

import strategyease_sdk

logging.basicConfig(level=logging.DEBUG)

client = strategyease_sdk.Client(host='localhost', port=8888, key='')
account_info = client.get_account('title:monijiaoyi')
print(account_info)
