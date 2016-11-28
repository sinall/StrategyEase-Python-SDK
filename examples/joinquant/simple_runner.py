# -*- coding: utf-8 -*-

import ConfigParser
import logging
import os

from shipane_sdk import Client
from shipane_sdk.joinquant.client import JoinQuantClient
from shipane_sdk.joinquant.runner import JoinQuantRunner

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)-6s %(message)s')

    dir_path = os.path.dirname(os.path.realpath(__file__))

    config = ConfigParser.RawConfigParser()
    config.read('{}/config/config.ini'.format(dir_path))

    shipane_client = Client(host=config.get('ShiPanE', 'host'),
                            port=config.get('ShiPanE', 'port'),
                            key=config.get('ShiPanE', 'key'))
    jq_client = JoinQuantClient(username=config.get('JoinQuant', 'username'),
                                password=config.get('JoinQuant', 'password'),
                                backtest_id=config.get('JoinQuant', 'backtestId'))
    jq_client.login()
    runner = JoinQuantRunner(shipane_client, jq_client, interval=15)

    runner.run()
