# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest


class StrTest(unittest.TestCase):
    def test_str(self):
        print(str(u'证券代码'.encode('utf-8')))
