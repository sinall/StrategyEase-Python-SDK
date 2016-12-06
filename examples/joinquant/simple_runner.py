# -*- coding: utf-8 -*-

import logging
import os

import six
from six.moves import configparser

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser

from shipane_sdk import Client
from shipane_sdk.joinquant.client import JoinQuantClient
from shipane_sdk.joinquant.runner import JoinQuantRunner

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)-6s %(message)s')

    dir_path = os.path.dirname(os.path.realpath(__file__))

    config = ConfigParser()
    config.read('{}/config/config.ini'.format(dir_path))

    shipane_client = Client(host=config.get('ShiPanE', 'host'),
                            port=config.get('ShiPanE', 'port'),
                            key=config.get('ShiPanE', 'key'))
    jq_client = JoinQuantClient(username=config.get('JoinQuant', 'username'),
                                password=config.get('JoinQuant', 'password'),
                                backtest_id=config.get('JoinQuant', 'backtest_id'))
    jq_client.login()
    runner = JoinQuantRunner(shipane_client, jq_client,
                             interval=config.getint('JoinQuant', 'interval'),
                             idle_interval=config.getint('JoinQuant', 'idle_interval'))

    runner.run()
