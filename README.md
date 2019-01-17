# KeePassHTTP

[![pypi](https://img.shields.io/pypi/v/keepasshttp.svg)](https://pypi.org/project/keepasshttp/)
[![python_versions](https://img.shields.io/pypi/pyversions/keepasshttp.svg)](https://pypi.org/project/keepasshttp/)
[![license](https://img.shields.io/github/license/cyrbil/python_keepass_http.svg)](https://github.com/cyrbil/python_keepass_http/blob/master/LICENSE.txt)
[![travis](https://img.shields.io/travis/cyrbil/python_keepass_http/master.svg)](https://travis-ci.org/cyrbil/python_keepass_http)
[![codecov.io](https://codecov.io/github/cyrbil/python_keepass_http/coverage.svg?branch=master)](https://codecov.io/github/cyrbil/python_keepass_http)


Python client for KeePassHTTP to interact with KeePass's credentials.


## Install

    pip install keepasshttp
    

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


## Configuration

This module will write to `~/.python_keepass_http` to save allowed AES key.
To change this path, instanciate `KeePassHTTP` with a different file.

    from keepasshttp import KeePassHTTP
    kph = KeePassHTTP('./keepass_key')
    
    
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