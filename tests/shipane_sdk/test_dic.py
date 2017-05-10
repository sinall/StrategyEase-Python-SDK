# -*- coding: utf-8 -*-

import unittest


class DictTest(unittest.TestCase):
    def test_modify_in_loop(self):
        data = dict(
            a=dict()
        )
        for key, value in data.items():
            value['b'] = 1
        print(data)
