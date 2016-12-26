# -*- coding: utf-8 -*-

import unittest

from shipane_sdk.stock import StockUtils


class StockUtilsTest(unittest.TestCase):
    def test_new_stocks(self):
        df = StockUtils.new_stocks()
        self.assertTrue((df.columns == ['code', 'xcode', 'name', 'ipo_date', 'price']).all())
