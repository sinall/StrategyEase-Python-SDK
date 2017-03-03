# -*- coding: utf-8 -*-

import logging

import shipane_sdk

logging.basicConfig(level=logging.DEBUG)

client = shipane_sdk.Client(host='localhost', port=8888, key='')
account_info = client.get_account('title:monijiaoyi')
print(account_info)
