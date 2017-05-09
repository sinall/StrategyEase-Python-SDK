# -*- coding: utf-8 -*-

from collections import OrderedDict


class MultiOrderedDict(OrderedDict):
    LIST_SUFFIX = '[]'
    LIST_SUFFIX_LEN = len(LIST_SUFFIX)

    def __setitem__(self, key, value):
        if key.endswith(self.LIST_SUFFIX):
            key = self.__normalize_key(key)
            values = super(MultiOrderedDict, self).setdefault(key, [])
            if isinstance(value, list):
                values.extend(value)
            else:
                values.append(value)
        else:
            super(MultiOrderedDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        is_multi = key.endswith(self.LIST_SUFFIX)
        if is_multi:
            key = self.__normalize_key(key)
        value = super(MultiOrderedDict, self).__getitem__(key)
        if is_multi and not isinstance(value, list):
            value = value.split('\n')
        return value

    def __normalize_key(self, key):
        return key[:-self.LIST_SUFFIX_LEN]
