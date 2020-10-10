#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class KeePassHTTPException(Exception):
    pass


class KeePassHTTPAssociationFailure(KeePassHTTPException):  # pragma: no cover
    def __init__(self, what):
        msg = "Fail to associate with KeePassHTTP, no {:s} id returned".format(what)
        super(KeePassHTTPAssociationFailure, self).__init__(msg)


class KeePassHTTPInvalidSignature(KeePassHTTPException):  # pragma: no cover
    def __init__(self):
        super(KeePassHTTPInvalidSignature, self).__init__("KeePassHTTP invalid signature")


class KeePassHTTPApplicationIdMismatch(KeePassHTTPException):  # pragma: no cover
    def __init__(self):
        super(KeePassHTTPApplicationIdMismatch, self).__init__("KeePassHTTP application id mismatch")


class KeePassHTTPDatabaseIdMismatch(KeePassHTTPException):  # pragma: no cover
    def __init__(self):
        super(KeePassHTTPDatabaseIdMismatch, self).__init__("KeePassHTTP database id mismatch")


class KeePassHTTPBadResponse(KeePassHTTPException):  # pragma: no cover
    def __init__(self, response):
        """`KeePassHTTPBadResponse` exception.

        :param response: :class:`Response <Response>` object
        :type response: requests.Response
        """
        self.response = response
        super(KeePassHTTPException, self).__init__("KeePassHTTP server return an error")

    def __str__(self):
        text = "{0:s}\nStatus: {1:d} - Body: {2:s}".format(
            super(KeePassHTTPException, self).__str__(),
            self.response.status_code,
            self.response.content.__repr__(),
        )
        print(text)
        return text
