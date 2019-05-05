# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import time


class MarketUtils(object):
    OPEN_TIME = time(9, 30)
    CLOSE_TIME = time(15)
    MIDDAY_CLOSE_TIME = time(11, 30)
    MIDDAY_OPEN_TIME = time(13)

    @classmethod
    def is_opening(cls, datetime_=None):
        if datetime_ is None:
            datetime_ = datetime.now()

        if datetime_.isoweekday() not in range(1, 6):
            return False
        if datetime_.time() <= cls.OPEN_TIME or datetime_.time() >= cls.CLOSE_TIME:
            return False
        if cls.MIDDAY_CLOSE_TIME <= datetime_.time() <= cls.MIDDAY_OPEN_TIME:
            return False
        return True

    @classmethod
    def is_closed(cls, datetime_=None):
        return not cls.is_opening(datetime_)
