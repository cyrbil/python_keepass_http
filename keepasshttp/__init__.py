#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .keepass_http import (
    AES_256_CBC,
    KeePassHTTP,
    KeePassHTTPCredential,
    KeePassHTTPException,
)


__VERSION__ = "1.2.1"


keepasshttp = KeePassHTTP()
get = keepasshttp.get
list = keepasshttp.list
create = keepasshttp.create
search = keepasshttp.search
update = keepasshttp.update
