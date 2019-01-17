#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from tests import mock

from unittest import TestCase
from keepasshttp import KeePassHTTP, KeePassHTTPCredential


class TestKeePassHTTP(TestCase):
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
        mock.RequestsMock.mock()
        mock.RandomBytesMock.mock()

    def validate_entry(self, entry):
        self.assertNotEqual(entry, None, "Entry should exist")
        self.assertTrue(
            isinstance(entry, KeePassHTTPCredential),
            "Entry should be a credential instance",
        )
        self.assertEqual(entry.password, "test", "Entry has invalid data")

    def test__register(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        storage = os.path.join(current_dir, "test_storage_tmp")
        if os.path.exists(storage):
            os.unlink(storage)
        try:
            self.kph = KeePassHTTP(storage)
            self.kph._load()
        finally:
            if os.path.exists(storage):
                os.unlink(storage)

    def test_get(self):
        entry = self.kph.get("get_url")
        self.validate_entry(entry)

        entry = self.kph.get("get_name")
        self.validate_entry(entry)

    def test_search(self):
        for search in ("search_url", "search_name"):
            entries = self.kph.search(search)
            self.assertEqual(
                len(entries), 2, "Unexpected number of result during search"
            )
            for entry in entries:
                self.validate_entry(entry)

    def test_list(self):
        self.kph.list()

    def test_update(self):
        entry = self.kph.update(
            "test", "test", "test", "1C23268FFA3AA847972641922BA3F611"
        )
        self.validate_entry(entry)

    def test_create(self):
        entry = self.kph.create("test", "test", "test")
        self.validate_entry(entry)
