# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import time


class MarketUtils(object):
    OPEN_TIME = time(9, 25)
    CLOSE_TIME = time(15)

    @classmethod
    def is_opening(cls, datetime_=None):
        if datetime_ is None:
            datetime_ = datetime.now()

        if datetime_.isoweekday() not in range(1, 6):
            return False
        if datetime_.time() <= cls.OPEN_TIME or datetime_.time() >= cls.CLOSE_TIME:
            return False
        return True

    @classmethod
    def is_closed(cls, datetime_=None):
        return not cls.is_opening(datetime_)
