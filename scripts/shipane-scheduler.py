#!/usr/bin/env python

import logging.config
import os

from shipane_sdk.scheduler import Scheduler

logging.config.fileConfig(os.path.join(os.path.expanduser('~'), '.shipane_sdk', 'config', 'logging.ini'))

Scheduler().start()
