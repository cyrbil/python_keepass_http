#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import six

# noinspection PyPackageRequirements
import Crypto.Random

# noinspection PyPackageRequirements
from Crypto.Cipher import AES

from requests.compat import str


# noinspection PyPep8Naming
class AES_256_CBC(object):
    def __init__(self, key, iv=None):
        if isinstance(key, str):  # pragma: no cover
            key = str(key).encode("utf-8")
        if isinstance(iv, str):  # pragma: no cover
            iv = str(iv).encode("utf-8")
        self.key = key
        self.iv = iv or self.rand_bytes(16)

    @staticmethod
    def rand_bytes(size):  # pragma: no cover
        return Crypto.Random.get_random_bytes(size)

    @staticmethod
    def pad(text):
        if not text:  # pragma: no cover
            return text
        if isinstance(text, str):
            text = str(text).encode("utf-8")
        to_pad = 16 - (len(text) % 16)
        return text + (six.int2byte(to_pad) * to_pad)

    @staticmethod
    def unpad(text):
        if not text:  # pragma: no cover
            return text
        val = six.byte2int(text[-1:])
        if val > 16:
            val = 0
        return text[: len(text) - val]

    def cipher(self):
        return AES.new(
            key=self.key, iv=self.iv, mode=AES.MODE_CBC,
        )

    def encrypt(self, text):
        padded_text = self.pad(text)
        cipher_text = self.cipher().encrypt(padded_text)
        return cipher_text

    def decrypt(self, ciphertext):
        padded_text = self.cipher().decrypt(ciphertext)
        text = self.unpad(padded_text)
        return text
