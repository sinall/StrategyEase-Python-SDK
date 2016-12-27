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
from shipane_sdk.jobs.joinquant_following import JoinQuantFollowingJob
from shipane_sdk.jobs.new_stock_purchase import NewStockPurchaseJob

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

        self._new_stock_purchase_job = NewStockPurchaseJob(self._config, self._client)
        self._joinquant_following_job = JoinQuantFollowingJob(self._config, self._client)

    def start(self):
        scheduler = BackgroundScheduler()

        if self._config.getboolean('NewStocks', 'enabled'):
            scheduler.add_job(self._new_stock_purchase_job,
                              APCronParser.parse(self._config.get('NewStocks', 'schedule')))
        else:
            self._log.warning('New stock purchase job is not enabled')

        if self._config.getboolean('JoinQuant', 'enabled'):
            scheduler.add_job(self._joinquant_following_job,
                              APCronParser.parse(self._config.get('JoinQuant', 'schedule')))
        else:
            self._log.warning('JoinQuant following job is not enabled')

        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
