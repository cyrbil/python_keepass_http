#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from unittest import TestCase

from tests import mock
from keepasshttp import KeePassHTTP
from keepasshttp.__main__ import cmd_line


output_text = """
404
test
  - login: test
  - password: test
  - name: test
  - url: None
  - id: 861BD08DED5C154C99AEBAFEBA48F739
  - fields: []
"""

output_table = """
credential	login	password	name	url 	id                              	fields
404       	     	        	    	    	                                	      
test      	test 	test    	test	None	861BD08DED5C154C99AEBAFEBA48F739	[]     
"""


output_python = """
{'404': None, 'test': {'login': 'test', 'password': 'test', 'name': 'test', 'url': None, 'id': '861BD08DED5C154C99AEBAFEBA48F739', 'fields': []}}
"""


output_json = """
{
  "404": null,
  "test": {
    "login": "test",
    "password": "test",
    "name": "test",
    "url": null,
    "id": "861BD08DED5C154C99AEBAFEBA48F739",
    "fields": []
  }
}
"""


output_csv = """
credential,login,password,name,url,id,fields
404,,,,,,
test,test,test,test,,861BD08DED5C154C99AEBAFEBA48F739,[]
"""


class TestCmdLine(TestCase):
    def setUp(self):
        if not os.getenv("TEST_WITH_KEEPASS", False):
            # mock http requests to run without KeePass
            mock.RequestsMock.mock()

        # mock random to be static and debuggable
        mock.RandomBytesMock.mock()

        current_dir = os.path.dirname(os.path.realpath(__file__))
        storage = os.path.join(current_dir, "test_storage")
        self.kph = KeePassHTTP(storage)

    def tearDown(self):
        mock.RequestsMock.unmock()
        mock.RandomBytesMock.unmock()

    def test_text(self):
        output = cmd_line(args=["404", "test"], kph=self.kph)
        self.compare_outputs(output, output_text)

    def test_json(self):
        output = cmd_line(args=["-f", "json", "404", "test"], kph=self.kph)
        self.compare_outputs(output, output_json)

    def test_csv(self):
        output = cmd_line(args=["-f", "csv", "404", "test"], kph=self.kph)
        self.compare_outputs(output, output_csv)

    def test_table(self):
        output = cmd_line(args=["-f", "table", "404", "test"], kph=self.kph)
        self.compare_outputs(output, output_table)

    def test_python(self):
        output = cmd_line(args=["-f", "python", "404", "test"], kph=self.kph)
        self.compare_outputs(output, output_python)

    def compare_outputs(self, output, output_expected):
        lines = output.strip().split()
        expected_lines = output_expected.strip().split()
        diff = set(lines).symmetric_difference(expected_lines)
        self.assertEqual(len(diff), 0, "Command line output has lines differences")
        for i, expected_line in enumerate(expected_lines):
            self.assertEqual(lines[i].strip(), expected_line.strip(), "Invalid command line output")