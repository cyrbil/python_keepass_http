#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import argparse

try:
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from ordereddict import OrderedDict

from keepasshttp import KeePassHTTP
from requests.compat import str


def python_fmt(entries):
    entries_dict = OrderedDict()
    for k, v in entries.items():
        if v:
            entry = OrderedDict((
                ("login", v.login),
                ("password", v.password),
                ("name", v.name),
                ("url", v.url),
                ("id", v.uuid),
                ("fields", v.string_fields),
            ))
        else:
            entry = None
        entries_dict[k] = entry
    return entries_dict


def text_fmt(entries):
    lines = []
    for k, credential in python_fmt(entries).items():
        lines.append(k)
        if credential:
            list(
                map(
                    lines.append, (
                        "  - {0}: {1}".format(field, value)
                        for field, value in credential.items()
                    ),
                ),
            )
    return '\n'.join(lines)


def json_fmt(entries):
    import json
    return json.dumps(python_fmt(entries), indent=2)


def csv_fmt(entries):
    def escape(s):
        return "\"{0}\"".format(str(s).replace("\"", "\\\""))

    output = []
    fields_header = ["credential", "login", "password", "name", "url", "id", "fields"]
    output.append(','.join(fields_header))
    for k, credential in python_fmt(entries).items():
        if credential:
            fields = [k] + list(credential.get(value, "") for value in fields_header[1:])
        else:
            fields = [k] + ([""]*6)
        output.append(','.join(map(escape, fields)))
    return '\n'.join(output)


def table_fmt(entries):
    lines_fields = [["credential", "login", "password", "name", "url", "id", "fields"]]
    max_fields_len = map(len, lines_fields[0])

    for k, credential in python_fmt(entries).items():
        if credential:
            credential_values = list(credential.get(value, "") for value in lines_fields[0][1:])
            line_fields = [k] + list(map(str, credential_values))
        else:
            line_fields = [k] + ([""]*6)
        max_fields_len = list(map(max, zip(max_fields_len, map(len, line_fields))))
        lines_fields.append(line_fields)

    return table_fmt_justify(lines_fields, max_fields_len)


def table_fmt_justify(lines_fields, max_fields_len):
    lines = []
    for line_fields in lines_fields:
        line = []
        for i, max_field_len in enumerate(max_fields_len):
            line.append(line_fields[i].ljust(max_field_len))
        lines.append('\t'.join(line))
    return '\n'.join(lines)


formatters = {
    "text": text_fmt,
    "table": table_fmt,
    "json": json_fmt,
    "csv": csv_fmt,
}


def cmd_line(args=None, kph=None):
    parser = argparse.ArgumentParser(prog="keepasshttp", description='Fetch credentials from keepass')
    parser.add_argument(
        '-c', '--config', dest='config_path',
        help="alternative path for keepasshttp's AES exchange key (default: ~/.python_keepass_http)",
    )
    parser.add_argument(
        '-u', '--url', default="http://localhost:19455/",
        help="alternative url for keepasshttp server (default: 'http://localhost:19455/')",
    )
    parser.add_argument(
        '-f', '--format', choices=formatters.keys(), default="text",
        help="output format for credentials",
    )
    parser.add_argument(
        'credentials', metavar='credential', nargs='+',
        help='Url or name to match credentials from keepass database',
    )
    args = parser.parse_args(args)

    # kph is only set for unittest
    if not kph:  # pragma: no cover
        kph = KeePassHTTP(storage=args.config_path, url=args.url)

    credentials = OrderedDict()
    for credential in args.credentials:
        credentials[credential] = kph.get(credential)

    return str(formatters[args.format](credentials))


if __name__ == "__main__":  # pragma: no cover
    print(cmd_line())
