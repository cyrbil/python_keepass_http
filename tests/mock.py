#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64

import requests

from keepasshttp import AES_256_CBC

data = {
    "associate":      b'{"RequestType":"associate","Success":true,"Id":"unittest_tmp","Count":0,"Version":"1.8.4.2",'
                      b'"Hash":"46e1d15ab37d8a2700b0c1755244433514b7a13f","Nonce":"SDfFtzkTrrrajXYfi0/wYA==",'
                      b'"Verifier":"kTRIa/0MyaSnD5cMvqMfnO4RUrVBKqxARO4tn858TzM="}',
    "test-associate": b'{"RequestType":"test-associate","Success":true,"Id":"unittest","Count":0,"Version":"1.8.4.2",'
                      b'"Hash":"46e1d15ab37d8a2700b0c1755244433514b7a13f","Nonce":"uVL8K1BgiMIPbl/tKNEB9Q==",'
                      b'"Verifier":"HEf6aOvr6zASN9ta3bXGu32CQQ1KT1LcXoCdihwjquQ="}',
    "get-logins":     b'{"RequestType":"get-logins","Success":true,"Id":"unittest","Count":1,"Version":"1.8.4.2",'
                      b'"Hash":"46e1d15ab37d8a2700b0c1755244433514b7a13f","Nonce":"RhejnJYTyrHLlqv2kWTGtQ==",'
                      b'"Verifier":"JibwoBzn/3JME1Srn/N6qsV/HknsrIiZDplkkvfbUcE=","Entries":[{'
                      b'"Login":"tK2twveV9rw4SSZdvmDd2g==","Password":"tK2twveV9rw4SSZdvmDd2g==",'
                      b'"Uuid":"/Vih5wfxi1v+ltJ7c3R35XhVCJCVApgINbhc7eK2Y/u8B78y2TB73avHbspjFopw",'
                      b'"Name":"tK2twveV9rw4SSZdvmDd2g==","StringFields":[]}, {"Login":"tK2twveV9rw4SSZdvmDd2g==",'
                      b'"Password":"tK2twveV9rw4SSZdvmDd2g==",'
                      b'"Uuid":"/Vih5wfxi1v+ltJ7c3R35XhVCJCVApgINbhc7eK2Y/u8B78y2TB73avHbspjFopw",'
                      b'"Name":"tK2twveV9rw4SSZdvmDd2g==","StringFields":[]}]}',
    "get-all-logins": b'{"RequestType":"get-all-logins","Success":true,"Id":"unittest","Count":1,"Version":"1.8.4.2",'
                      b'"Hash":"46e1d15ab37d8a2700b0c1755244433514b7a13f","Nonce":"RhejnJYTyrHLlqv2kWTGtQ==",'
                      b'"Verifier":"JibwoBzn/3JME1Srn/N6qsV/HknsrIiZDplkkvfbUcE=","Entries":[{'
                      b'"Login":"tK2twveV9rw4SSZdvmDd2g==","Password":"tK2twveV9rw4SSZdvmDd2g==",'
                      b'"Uuid":"/Vih5wfxi1v+ltJ7c3R35XhVCJCVApgINbhc7eK2Y/u8B78y2TB73avHbspjFopw",'
                      b'"Name":"tK2twveV9rw4SSZdvmDd2g==","StringFields":[]}, {"Login":"tK2twveV9rw4SSZdvmDd2g==",'
                      b'"Password":"tK2twveV9rw4SSZdvmDd2g==",'
                      b'"Uuid":"/Vih5wfxi1v+ltJ7c3R35XhVCJCVApgINbhc7eK2Y/u8B78y2TB73avHbspjFopw",'
                      b'"Name":"tK2twveV9rw4SSZdvmDd2g==","StringFields":[]}]}',
    "set-login":      b'{"RequestType":"set-login", "Success":true,"Id":"unittest","Count":0,"Version":"1.8.4.2",'
                      b'"Hash":"46e1d15ab37d8a2700b0c1755244433514b7a13f","Nonce":"9MDKT27u19P2iDvYHArldw==",'
                      b'"Verifier":"qb4TcljmB+bgJhbMe7KZ256enks+ewMrlXY9IB63+KI="}',
}


class RequestsMock(object):
    mocked = None

    @classmethod
    def mock(cls):
        cls.mocked = requests.post

        def post(json, *_, **__):
            rt = json.get("RequestType")
            content = data[rt]
            response = requests.Response()
            response._content = content
            response._content_consumed = True
            response.status_code = 200
            return response

        requests.post = post

    @classmethod
    def unmock(cls):
        if cls.mocked:
            requests.post = cls.mocked


class RandomBytesMock(object):
    mocked = None

    @classmethod
    def mock(cls):
        cls.mocked = AES_256_CBC.rand_bytes

        def rand_bytes(n, *args, **kwargs):
            if n is 16:
                return base64.b64decode(b'DEBUG+16+CtERUJVRysxNg==')
            elif n is 32:
                return base64.b64decode(b'DEBUG+256+bits++++srKysrREVCVUcrMjU2K2JpdHM=')
            else:
                return cls.mocked(n=n, *args, **kwargs)

        AES_256_CBC.rand_bytes = staticmethod(rand_bytes)

    @classmethod
    def unmock(cls):
        if cls.mocked:
            AES_256_CBC.rand_bytes = cls.mocked
