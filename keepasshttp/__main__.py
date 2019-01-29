#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from keepasshttp import KeePassHTTP


def python_fmt(entries):
    return {
        k: {
            "login": v.login,
            "password": v.password,
            "name": v.name,
            "url": v.url,
            "id": v.uuid,
            "fields": v.string_fields,
        } if v else None
        for k, v in entries.items()
    }


def text_fmt(entries):
    lines = []
    for k, credential in python_fmt(entries).items():
        lines.append(k)
        if credential:
            for field, value in credential.items():
                lines.append("  - {0}: {1}".format(field, value))
    return '\n'.join(lines)


def json_fmt(entries):
    import json
    return json.dumps(python_fmt(entries), indent=2)


def csv_fmt(entries):
    import io
    import csv

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["credential", "login", "password", "name", "url", "id", "fields"])
    for k, credential in python_fmt(entries).items():
        if credential:
            writer.writerow([k, *credential.values()])
        else:
            writer.writerow([k, *[""]*6])
    return output.getvalue()


def table_fmt(entries):
    lines_fields = [["credential", "login", "password", "name", "url", "id", "fields"]]
    max_fields_len = map(len, lines_fields[0])

    for k, credential in python_fmt(entries).items():
        if credential:
            line_fields = [k, *map(str, credential.values())]
        else:
            line_fields = [k, *[""]*6]
        max_fields_len = list(map(max, zip(max_fields_len, map(len, line_fields))))
        lines_fields.append(line_fields)

    lines = []
    for line_fields in lines_fields:
        line = []
        for i, max_field_len in enumerate(max_fields_len):
            line.append(line_fields[i].ljust(max_field_len))
        lines.append('\t'.join(line))
    return '\n'.join(lines)


formatters = {
    "python": python_fmt,
    "text": text_fmt,
    "table": table_fmt,
    "json": json_fmt,
    "csv": csv_fmt
}


def cmd_line(args=None, kph=None):
    parser = argparse.ArgumentParser(prog="keepasshttp", description='Fetch credentials from keepass')
    parser.add_argument('-c', '--config', dest='config_path',
                        help="alternative path for keepasshttp's AES exchange key (default: ~/.python_keepass_http)")
    parser.add_argument('-u', '--url', default="http://localhost:19455/",
                        help="alternative url for keepasshttp server (default: 'http://localhost:19455/')")
    parser.add_argument('-f', '--format', choices=formatters.keys(), default="text",
                        help="output format for credentials")
    parser.add_argument('credentials', metavar='credential', nargs='+',
                        help='Url or name to match credentials from keepass database')
    args = parser.parse_args(args)

    # kph is only set for unittest
    if not kph:  # pragma: no cover
        kph = KeePassHTTP(storage=args.config_path, url=args.url)

    credentials = {
        credential: kph.get(credential)
        for credential in args.credentials
    }

    return str(formatters[args.format](credentials))


if __name__ == "__main__":  # pragma: no cover
    print(cmd_line())
