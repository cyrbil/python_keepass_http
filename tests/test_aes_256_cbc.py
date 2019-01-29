#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

from unittest import TestCase
from keepasshttp import AES_256_CBC


class TestKeePassHTTP(TestCase):
    IV = b"\x0c@T\x1b\xedz\xf8+DEBUG+16"
    KEY = b"\x0c@T\x1b\xed\xb9\xeb\xe6\xe2\xb6\xcf\xbe\xfb\xeb++++DEBUG+256+bits"

    def test_encrypt(self):
        aes = AES_256_CBC(self.KEY, self.IV)
        cipher_text = aes.encrypt("Hello World !")
        self.assertEqual(
            cipher_text,
            b"GD@\"\xdb\xb6\x1f\xe5\xef\x92?[p\x99\xf1\x1f",
            "AES encryption produced unexpected result")

        # ensure long text is also rightly treated (iv changes)
        cipher_text = aes.encrypt("Hello World !" * 100000)
        digest_cipher_text = hashlib.sha1(cipher_text).hexdigest()
        self.assertEqual(
            digest_cipher_text,
            "ba0033d46d20113c2aed3f9eb059f9c885414cdc",
            "AES encryption produced unexpected result")

    def test_decrypt(self):
        aes = AES_256_CBC(self.KEY, self.IV)
        cipher_text = aes.decrypt(b"Hello World !!!!")
        self.assertEqual(
            cipher_text,
            b"\xc9#\xbf.\xc6\xe5\xaf\x868'N\xba\xfe\xa5\x91l",
            "AES decryption produced unexpected result")

        # ensure long text is also rightly treated (iv changes)
        cipher_text = aes.decrypt(b"Hello World !!!!" * 100000)
        digest_cipher_text = hashlib.sha1(cipher_text).hexdigest()
        self.assertEqual(
            digest_cipher_text,
            "6335686444663cbeffbd9543db7b1ebc17bbe4ac",
            "AES decryption produced unexpected result")
