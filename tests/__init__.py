#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover(".")
    unittest.TextTestRunner().run(all_tests)
