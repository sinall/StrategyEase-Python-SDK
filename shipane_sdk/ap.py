# -*- coding: utf-8 -*-

from apscheduler.triggers.cron import CronTrigger


class APCronParser(object):
    @classmethod
    def parse(cls, expression):
        parts = list(reversed(expression.split()))
        for i in range(len(parts)):
            if parts[i] == '?':
                parts[i] = None

        return CronTrigger(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7])
