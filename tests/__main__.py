#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import unittest
    all_tests = unittest.TestLoader().discover(".")
    unittest.TextTestRunner().run(all_tests)
