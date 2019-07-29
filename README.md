# KeePassHTTP

[![pypi_version.svg][pypi_version.svg]][pypi_project.url]
[![pypi_status.svg][pypi_status.svg]][pypi_project.url]
[![pypi_format.svg][pypi_format.svg]][pypi_project.url]
[![python_versions.svg][python_versions.svg]][pypi_project.url]
[![license.svg][license.svg]][license.url]
[![Maintainability][maintainability.svg]][maintainability.url]
[![travis_build.svg][travis_build.svg]][travis.url]
[![codecov.svg][codecov.svg]][codecov.url]
[![requirements_status.svg][requirements_status.svg]][requires.url]
[![code_size.svg][code_size.svg]][pypi_project.url]
[![pypi_downloads.svg][pypi_downloads.svg]][pypi_project.url]


Python client for [KeePassHTTP][keepasshttp.url] to interact with [KeePass][keepass.url]'s credentials.


## Install

    $ pip install keepasshttp


## Usage

    import keepasshttp

    # get single credential
    credential = keepasshttp.get("my_credential_name_or_url")
    print(credential.login)
    print(credential.password)

    # find all credentials's name
    credentials = keepasshttp.list()

    # fetch all partiall matching credentials
    credentials = keepasshttp.search("my_credential_name_or_url")

    # create a new keepasshttp entry
    keepasshttp.create("login", "password", "url")

    # update a keepasshttp entry
    credential.password = "new password"
    # or
    keepasshttp.update("login", "password", "url", "uuid")


## Command line

KeePassHTTP can also be called from command line:


    $ python -m keepasshttp --help
    usage: keepasshttp [-h] [-c CONFIG_PATH] [-u URL]
                   [-f {python,text,table,json,csv}]
                   credential [credential ...]

    Fetch credentials from keepass

    positional arguments:
      credential            Url or name to match credentials from keepass database

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_PATH, --config CONFIG_PATH
                            alternative path for keepasshttp's AES exchange key
                            (default: ~/.python_keepass_http)
      -u URL, --url URL     alternative url for keepasshttp server (default:
                            'http://localhost:19455/')
      -f {python,text,table,json,csv}, --format {python,text,table,json,csv}
                            output format for credentials

    $ python -m keepathhttp my_credential_name_or_url
    my_credential_name_or_url
      - login: login
      - password: password
      - name: test
      - url: my_credential_name_or_url
      - id: ABCDEF1234567890ABCDEF1234567890
      - fields: []


## Configuration

By default, this module will write AES association key to `~/.python_keepass_http`
and use `http://localhost:19455/` to connect to the [KeePassHTTP][keepasshttp.url] server.

To change theses parameters, instantiate `keepasshttp.KeePassHTTP` class with different values.

    from keepasshttp import KeePassHTTP
    kph = KeePassHTTP(
        storage="./keepasshttp_key",
        url="https://example.com:1337/")
    kph.get("...")
    ...


## Testing

You can simply run the tests using:

    python -m unittest discover

`KeePassHTTP` calls are mocked, to run the tests against a real server, you need to:

   - open `tests/test_database.kdbx` in `KeePass` password is `test`
   - set `TEST_WITH_KEEPASS` environment variable
   - run test normally


## Coverage

To run tests with coverage:

    pip install pytest-cov
    pytest --cov


[comment]: # (Urls references)
[pypi_project.url]: https://pypi.org/project/keepasshttp/
[license.url]: ./LICENSE.txt
[travis.url]: https://travis-ci.org/cyrbil/python_keepass_http
[codecov.url]: https://codecov.io/github/cyrbil/python_keepass_http
[requires.url]: https://requires.io/github/cyrbil/python_keepass_http/requirements/?branch=master
[keepasshttp.url]: https://github.com/pfn/keepasshttp
[keepass.url]: https://keepass.info/
[maintainability.url]: https://codeclimate.com/github/cyrbil/python_keepass_http/maintainability

[comment]: # (Images references)
[pypi_version.svg]: https://img.shields.io/pypi/v/keepasshttp.svg "PYPI KeePassHTTP"
[pypi_status.svg]: https://img.shields.io/pypi/status/keepasshttp.svg "PYPI KeePassHTTP"
[pypi_format.svg]: https://img.shields.io/pypi/format/keepasshttp.svg "PYPI KeePassHTTP"
[python_versions.svg]: https://img.shields.io/pypi/pyversions/keepasshttp.svg "PYPI KeePassHTTP"
[license.svg]: https://img.shields.io/github/license/cyrbil/python_keepass_http.svg "MIT"
[travis_build.svg]: https://img.shields.io/travis/cyrbil/python_keepass_http/master.svg "travis.org"
[codecov.svg]: https://codecov.io/github/cyrbil/python_keepass_http/coverage.svg?branch=master "codecov.io"
[requirements_status.svg]: https://img.shields.io/requires/github/cyrbil/python_keepass_http.svg "requires.io"
[code_size.svg]: https://img.shields.io/github/languages/code-size/cyrbil/python_keepass_http.svg "All files"
[pypi_downloads.svg]: https://img.shields.io/pypi/dm/keepasshttp.svg "PYPI KeePassHTTP"
[maintainability.svg]: https://api.codeclimate.com/v1/badges/9aa1b086f9dde4d1e23d/maintainability
