# -*- coding: utf-8 -*-

import unittest

from shipane_sdk.support import Struct


class StructTest(unittest.TestCase):
    def test_init(self):
        config = Struct({"key": "value"})
        self.assertEquals(config.key, "value")
