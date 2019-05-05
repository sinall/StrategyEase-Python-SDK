# -*- coding: utf-8 -*-

import datetime
from collections import OrderedDict

import yaml


class Struct(object):
    def __init__(self, data):
        for key, value in data.items():
            key = key.replace('-', '_')
            if isinstance(value, tuple):
                setattr(self, key, (Struct(x) if isinstance(x, dict) else x for x in value))
            if isinstance(value, list):
                setattr(self, key, [Struct(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, Struct(value) if isinstance(value, dict) else value)


class OrderedDictYAMLLoader(yaml.Loader):
    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_odict)

    def construct_odict(self, node):
        omap = OrderedDict()
        yield omap
        if not isinstance(node, yaml.SequenceNode):
            raise yaml.constructor.ConstructorError(
                "while constructing an ordered map",
                node.start_mark,
                "expected a sequence, but found %s" % node.id, node.start_mark
            )
        for subnode in node.value:
            if not isinstance(subnode, yaml.MappingNode):
                raise yaml.constructor.ConstructorError(
                    "while constructing an ordered map", node.start_mark,
                    "expected a mapping of length 1, but found %s" % subnode.id,
                    subnode.start_mark
                )
            if len(subnode.value) != 1:
                raise yaml.constructor.ConstructorError(
                    "while constructing an ordered map", node.start_mark,
                    "expected a single mapping item, but found %d items" % len(subnode.value),
                    subnode.start_mark
                )
            key_node, value_node = subnode.value[0]
            key = self.construct_object(key_node)
            value = self.construct_object(value_node)
            omap[key] = value


class StopWatch(object):
    def __init__(self):
        pass

    def start(self):
        self._start_time = datetime.datetime.now()

    def stop(self):
        self._end_time = datetime.datetime.now()
        return self

    def short_summary(self):
        return str(self._end_time - self._start_time)
