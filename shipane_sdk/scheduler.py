# -*- coding: utf-8 -*-
import codecs
import logging
import os
import os.path
import time

import six
from apscheduler.schedulers.background import BackgroundScheduler
from six.moves import configparser

from shipane_sdk import Client
from shipane_sdk.ap import APCronParser
from shipane_sdk.jobs.new_stock_purchase import NewStockPurchaseJob
from shipane_sdk.jobs.online_quant_following import OnlineQuantFollowingJob
from shipane_sdk.joinquant.client import JoinQuantClient
from shipane_sdk.ricequant.client import RiceQuantClient

if six.PY2:
    ConfigParser = configparser.RawConfigParser
else:
    ConfigParser = configparser.ConfigParser


class Scheduler(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)-6s %(message)s')
        self._log = logging.getLogger()

        config_path = os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config', 'scheduler.ini')
        self._log.info('Config path: %s', config_path)
        self._config = ConfigParser()
        self._config.readfp(codecs.open(config_path, "r", "utf8"))

        self._client = Client(host=self._config.get('ShiPanE', 'host'),
                              port=self._config.get('ShiPanE', 'port'),
                              key=self._config.get('ShiPanE', 'key'))
        self._jq_client = JoinQuantClient(username=self._config.get('JoinQuant', 'username'),
                                          password=self._config.get('JoinQuant', 'password'),
                                          backtest_id=self._config.get('JoinQuant', 'backtest_id'))
        self._rq_client = RiceQuantClient(username=self._config.get('RiceQuant', 'username'),
                                          password=self._config.get('RiceQuant', 'password'),
                                          run_id=self._config.get('RiceQuant', 'run_id'))

        self._new_stock_purchase_job = NewStockPurchaseJob(self._config, self._client)
        self._jq_following_job = OnlineQuantFollowingJob(self._client, self._jq_client, 'JoinQuantFollowingJob')
        self._rq_following_job = OnlineQuantFollowingJob(self._client, self._rq_client, 'RiceQuantFollowingJob')

    def start(self):
        scheduler = BackgroundScheduler()

        if self._config.getboolean('NewStocks', 'enabled'):
            scheduler.add_job(self._new_stock_purchase_job,
                              APCronParser.parse(self._config.get('NewStocks', 'schedule')))
        else:
            self._log.warning('New stock purchase job is not enabled')

        if self._config.getboolean('JoinQuant', 'enabled'):
            scheduler.add_job(self._jq_following_job,
                              APCronParser.parse(self._config.get('JoinQuant', 'schedule')),
                              None, None, None, self._jq_following_job.name)
        else:
            self._log.warning('JoinQuant following job is not enabled')

        if self._config.getboolean('RiceQuant', 'enabled'):
            scheduler.add_job(self._rq_following_job,
                              APCronParser.parse(self._config.get('RiceQuant', 'schedule')),
                              None, None, None, self._rq_following_job.name)
        else:
            self._log.warning('RiceQuant following job is not enabled')

        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
