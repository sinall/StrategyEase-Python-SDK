# -*- coding: utf-8 -*-

import re

from hamcrest.core.base_matcher import BaseMatcher


class HasColumn(BaseMatcher):
    def __init__(self, column):
        self._column = column

    def _matches(self, df):
        return self._column in df.columns

    def describe_to(self, description):
        description.append_text(u'Dataframe doesn\'t have colum [{0}]'.format(self._column))


def has_column(column):
    return HasColumn(column)


class HasColumnMatches(BaseMatcher):
    def __init__(self, column_pattern):
        self._column_pattern = re.compile(column_pattern)

    def _matches(self, df):
        return len(list(filter(self._column_pattern.match, df.columns.values))) > 0

    def describe_to(self, description):
        description.append_text(u'Dataframe doesn\'t have colum matches [{0}]'.format(self._column_pattern))


def has_column_matches(column_pattern):
    return HasColumnMatches(column_pattern)


class HasRow(BaseMatcher):
    def __init__(self, row):
        self._row = row

    def _matches(self, df):
        return self._row in df.index

    def describe_to(self, description):
        description.append_text(u'Dataframe doesn\'t have row [%s]'.format(self._row))


def has_row(row):
    return HasRow(row)
