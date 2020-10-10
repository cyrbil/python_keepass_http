#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class KeePassHTTPCredential(object):
    def __init__(self, kph, entry):
        self.kph = kph
        self.name = entry.get("Name")
        self.uuid = entry.get("Uuid")
        self._login = entry.get("Login")
        self._password = entry.get("Password")
        self.string_fields = entry.get("StringFields") or []
        # never received, put can be updated
        self._url = None

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password

    @property
    def url(self):
        return self._url

    @login.setter
    def login(self, value):
        self._login = value
        self.update()

    @password.setter
    def password(self, value):
        self._password = value
        self.update()

    @url.setter
    def url(self, value):
        self._url = value
        self.update()

    def update(self):
        self.kph.update(
            uid=self.uuid,
            login=self._login,
            password=self._password,
            url=self._url,
        )

    def __repr__(self):  # pragma: no cover
        text = "<{0:s}[{1:s},{2:s}] at {3:s}>".format(
            self.__class__.__name__,
            self.name,
            self.uuid,
            hex(self.__hash__()),
        )
        return text
