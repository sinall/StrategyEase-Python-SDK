# -*- coding: utf-8 -*-

import importlib.util
import os
import unittest


class ConfigInstantiatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_config_instantiation(self):
        setup_module_file_location = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
        spec = importlib.util.spec_from_file_location("setup", setup_module_file_location)
        setup = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(setup)

        path = os.path.join(os.path.dirname(__file__), 'resources', 'example-config')
        concrete_file_path = os.path.join(path, 'b.ini')
        if os.path.isfile(concrete_file_path):
            os.remove(concrete_file_path)
            setup.ConfigInstantiator.instantiate(path)
        self.assertTrue(os.path.isfile(concrete_file_path))
