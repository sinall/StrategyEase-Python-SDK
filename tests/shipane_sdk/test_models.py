# -*- coding: utf-8 -*-

import unittest

from shipane_sdk.models import *


class OrderTest(unittest.TestCase):
    def test_str(self):
        order = Order(action=OrderAction.OPEN, security='000001', amount=100, price=10.1, style=OrderStyle.LIMIT)
        print(order)
        order.price = 417.48
        print(order)
