#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import base64

import six
import requests

# noinspection PyCompatibility
from requests.compat import str, bytes

from .aes_256_cbc import AES_256_CBC


class KeePassHTTPSingleton(type):
    _instances = {}

    def __call__(cls, storage=None, *args, **kwargs):
        key = (cls, storage)
        instance = cls._instances.get(key)
        if not instance:
            instance = cls._instances[key] = super(KeePassHTTPSingleton, cls).__call__(storage, *args, **kwargs)
        return instance


class KeePassHTTPCredential(object):
    def __init__(self, entry):
        self.name = entry.get("Name")
        self.uuid = entry.get("Uuid")
        self.login = entry.get("Login")
        self.password = entry.get("Password")
        self.string_fields = entry.get("StringFields") or []


class KeePassHTTPException(Exception):
    pass


class KeePassHTTP(six.with_metaclass(KeePassHTTPSingleton, object)):
    instances = {}
    encrypted_fields = ("Verifier", "Url", "SubmitUrl", "Login", "Password", "Uuid")
    default_storage = os.path.expanduser(os.path.join("~", ".python_keepass_http"))

    def __init__(self, storage=None, url="http://localhost:19455/"):
        """KeePassHTTP easy wrapper

        :param storage: file path to store private association key
                        (default to "~/.python_keepass_http")
        :type storage: str
        """
        self.url = url
        self.uid = None
        self.key = None
        self.db_hash = None
        self.storage = storage
        if not self.storage:
            self.storage = self.default_storage

    def search(self, key, sort_keys=False):
        """Search all matching entries for a given ``key``.
        For every entry, the Levenshtein Distance of his Entry-URL (or Title, if Entry-URL is not set)
        to the ``key`` is calculated. Only the entries with the minimal distance are returned

        :param key: partial key to look for, it will match url or title fields in KeePass
        :type key: str
        :param sort_keys: sort results
        :type sort_keys: bool
        :return: Credentials list
        :rtype: List[KeePassHTTPCredential]
        """
        data = self._request("get-logins", Url=key, SortSelection=sort_keys)
        entries = []
        for entry in data.get("Entries", ()):
            entries.append(KeePassHTTPCredential(entry))
        return entries

    def get(self, key):
        """Search all matching entries for a given ``key``.
        For every entry, the Levenshtein Distance of his Entry-URL (or Title, if Entry-URL is not set)
        to the ``key`` is calculated. Only the entry with the minimal distance are returned

        :param key: partial key to look for, it will match url or title fields in KeePass
        :type key: str
        :return: Credential
        :rtype: KeePassHTTPCredential
        """
        entries = self.search(key)
        return entries[0] if entries else None

    def list(self):
        data = self._request("get-all-logins")
        entries = []
        for entry in data.get("Entries", ()):
            entries.append(KeePassHTTPCredential(entry))
        return entries

    def update(self, login, password, url, uid=None):
        data = self._request("set-login", Login=login, Password=password, Url=url, Uuid=uid)
        return self.get(data.get("Id"))

    def create(self, login, password, url):
        return self.update(login, password, url)

    def _load(self):
        if not os.path.exists(self.storage):
            self.key = AES_256_CBC.rand_bytes(32)
            self.uid, self.db_hash = self._register()
            with open(self.storage, "wb+") as fd:
                data = b'\n'.join((
                    base64.b64encode(self.uid.encode("utf-8")),
                    base64.b64encode(self.key),
                    base64.b64encode(self.db_hash.encode("utf-8"))
                ))
                fd.write(data)
        else:
            with open(self.storage, "rb") as fd:
                data = fd.read()
                uid, self.key, db_hash = map(base64.b64decode, data.split())
                self.uid = uid.decode("utf-8")
                self.db_hash = db_hash.decode("utf-8")
            self._authenticate()

    def _register(self):
        data = self._request("associate", Key=base64.b64encode(self.key))
        uid = data.get("Id")
        if not uid:
            raise KeePassHTTPException("Fail to associate with KeePassHTTP, no app id returned")
        db_hash = data.get("Hash")
        if not db_hash:
            raise KeePassHTTPException("Fail to associate with KeePassHTTP, no db_hash returned")
        return uid, db_hash

    def _authenticate(self):
        self._request("test-associate")

    def _request(self, request, **request_data):
        if not self.key:
            self._load()

        aes = AES_256_CBC(self.key)
        iv = base64.b64encode(aes.iv)

        request_data.update({
            "RequestType": request,
            "Id": self.uid,
            "Nonce": iv,
            "Verifier": iv
        })

        request_data = self._encrypt(aes, request_data)

        response = requests.post(
            url=self.url,
            json=request_data
        )
        if response.status_code is not 200:
            raise KeePassHTTPException("KeePassHTTP returned an error")

        response_data = response.json()
        if not response_data.get("Success", False):
            raise KeePassHTTPException("KeePassHTTP returned an error")

        nonce = response_data.get("Nonce", "")
        iv = base64.b64decode(nonce)

        aes = AES_256_CBC(self.key, iv)
        signature = base64.b64decode(response_data.get("Verifier", ""))
        verifier = aes.decrypt(signature).decode("utf-8")

        if nonce != verifier:
            raise KeePassHTTPException("KeePassHTTP invalid signature")
        if self.uid and self.uid != response_data.get("Id"):
            raise KeePassHTTPException("KeePassHTTP application id mismatch")
        if self.db_hash and self.db_hash != response_data.get("Hash"):
            raise KeePassHTTPException("KeePassHTTP database id mismatch")

        response_data = self._decrypt(aes, response_data)
        return response_data

    def _encrypt(self, aes, data):
        if isinstance(data, bytes):
            data = data.decode("utf-8")

        elif isinstance(data, dict):
            for key, value in list(data.items()):
                if value is None:
                    del data[key]
                    continue
                if key in self.encrypted_fields and isinstance(value, (bytes, str)):
                    cipher_value = aes.encrypt(value)
                    value = base64.b64encode(cipher_value)
                value = self._encrypt(aes, value)
                data[key] = value

        elif not isinstance(data, str):
            if hasattr(data, "__iter__"):  # pragma: no cover
                encrypted_data = []
                for item in data:
                    encrypted_data.append(self._encrypt(aes, item))
                data = encrypted_data
            else:
                data = str(data).lower()

        return data

    def _decrypt(self, aes, data):
        if isinstance(data, str):
            # noinspection PyBroadException
            try:
                data = aes.decrypt(base64.b64decode(data)).decode("utf-8")
            except Exception:
                pass

        elif isinstance(data, dict):
            for key, value in data.items():
                data[key] = self._decrypt(aes, value)

        elif hasattr(data, "__iter__"):
            decrypted_data = []
            for item in data:
                decrypted_data.append(self._decrypt(aes, item))
            data = decrypted_data
        return data
