# -*- coding: utf-8 -*-

import codecs
import collections
import distutils.util
import errno
import logging
import logging.config
import logging.handlers
import os
import os.path
import time

from apscheduler.schedulers.background import BackgroundScheduler
from six.moves import configparser

from shipane_sdk import Client
from shipane_sdk.ap import APCronParser
from shipane_sdk.guorn.client import GuornClient
from shipane_sdk.jobs.batch import BatchJob
from shipane_sdk.jobs.new_stock_purchase import NewStockPurchaseJob
from shipane_sdk.jobs.online_quant_following import OnlineQuantFollowingJob
from shipane_sdk.jobs.online_quant_sync import OnlineQuantSyncJob
from shipane_sdk.jobs.repo import RepoJob
from shipane_sdk.joinquant.client import JoinQuantClient
from shipane_sdk.ricequant.client import RiceQuantClient
from shipane_sdk.uqer.client import UqerClient


class Scheduler(object):
    def __init__(self):
        self._logger = logging.getLogger()

        config_path = os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config', 'scheduler.ini')
        self._logger.info('Config path: %s', config_path)
        self._config = configparser.RawConfigParser()
        self._config.readfp(codecs.open(config_path, encoding="utf_8_sig"), )

        self._scheduler = BackgroundScheduler()
        self._client = Client(self._logger, **dict(self._config.items('ShiPanE')))

    def start(self):
        self.__add_job(self.__create_new_stock_purchase_job())
        self.__add_job(self.__create_repo_job())
        self.__add_job(self.__create_batch_job())
        self.__add_job(self.__create_join_quant_following_job())
        self.__add_job(self.__create_rice_quant_following_job())
        self.__add_job(self.__create_uqer_following_job())
        self.__add_job(self.__create_guorn_sync_job())
        self.__add_job(self.__create_join_quant_sync_job())

        self._scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self._scheduler.shutdown()

    def __add_job(self, job):
        if job.is_enabled:
            self._scheduler.add_job(job, APCronParser.parse(job.schedule), name=job.name, misfire_grace_time=None)
        else:
            self._logger.warning('{} is not enabled'.format(job.name))

    def __create_new_stock_purchase_job(self):
        section = 'NewStocks'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        return NewStockPurchaseJob(self._client, client_aliases, '{}Job'.format(section), **options)

    def __create_repo_job(self):
        section = 'Repo'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        return RepoJob(self._client, client_aliases, '{}Job'.format(section), **options)

    def __create_batch_job(self):
        section = 'Batch'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        return BatchJob(self._client, client_aliases, '{}Job'.format(section), **options)

    def __create_join_quant_following_job(self):
        section = 'JoinQuant'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        quant_client = JoinQuantClient(**options)
        return OnlineQuantFollowingJob(self._client, quant_client, client_aliases, '{}FollowingJob'.format(section),
                                       **options)

    def __create_rice_quant_following_job(self):
        section = 'RiceQuant'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        quant_client = RiceQuantClient(**options)
        return OnlineQuantFollowingJob(self._client, quant_client, client_aliases, '{}FollowingJob'.format(section),
                                       **options)

    def __create_uqer_following_job(self):
        section = 'Uqer'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        quant_client = UqerClient(**options)
        return OnlineQuantFollowingJob(self._client, quant_client, client_aliases, '{}FollowingJob'.format(section),
                                       **options)

    def __create_guorn_sync_job(self):
        section = 'Guorn'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        quant_client = GuornClient(**options)
        return OnlineQuantSyncJob(self._client, quant_client, client_aliases, '{}SyncJob'.format(section),
                                  **options)

    def __create_join_quant_sync_job(self):
        section = 'JoinQuantArena'
        options = self.__build_options(section)
        client_aliases = self.__filter_client_aliases(section)
        quant_client = JoinQuantClient(**options)
        return OnlineQuantSyncJob(self._client, quant_client, client_aliases, '{}SyncJob'.format(section),
                                  **options)

    def __build_options(self, section):
        if not self._config.has_section(section):
            return dict()

        options = dict(self._config.items(section))
        options['enabled'] = bool(distutils.util.strtobool(options['enabled']))
        return options

    def __filter_client_aliases(self, section):
        if not self._config.has_section(section):
            return dict()

        all_client_aliases = dict(self._config.items('ClientAliases'))
        client_aliases = [client_alias.strip() for client_alias in
                          filter(None, self._config.get(section, 'clients').split(','))]
        return collections.OrderedDict(
            (client_alias, all_client_aliases[client_alias]) for client_alias in client_aliases)


class FileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, fileName):
        path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', '爱股网', '实盘易')
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
        super(FileHandler, self).__init__(path + "/" + fileName)


def start():
    logging.config.fileConfig(os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config', 'logging.ini'))

    Scheduler().start()
