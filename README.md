# kumaone

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![PyPI - Version](https://img.shields.io/pypi/v/kumaone.svg)](https://pypi.org/project/kumaone)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kumaone.svg)](https://pypi.org/project/kumaone)

-----

**Table of Contents**

- [Virtualenv](#virtualenv)
- [Installation](#installation)
- [License](#license)
- [Features](#features)

## Virtualenv

- Install `pipenv` from [here](https://pipenv.pypa.io/en/latest/installation/)

- Activate virtual environment

  ```shell
  pipenv shell
  ```

  > if there are no virtual environment available (e.g. first use), a virtual environment will created and activated
    automatically.

- Install dependencies

  To install dependencies with `pipenv` use the following command

  ```shell
  pipenv install
  ```

  To install `dev` dependencies use `--dev` flag

  ```shell
  pipenv install --dev
  ```

## Installation

```shell
pip install kumaone
```

## Installation (Dev)

```shell
pip install -e .
```

## License

`kumaone` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Features

### Info

- [x] Show information about `kumaone`

### Configuration

- [x] Show `uptime kuma` configuration (default/custom paths)
- [x] Create `uptime kuma` configuration (default/custom path)
- [x] Delete `uptime kuma` configuration
- [ ] Edit `uptime kuma` configuration

### Monitors

- [x] List all monitors. `groups` and `processes` also.
- [x] Bulk `add` monitors from file(s)
- [ ] Don't stop the program if one monitor process runs into error
- [ ] Add debug logs for methods
- [x] Bulk `delete` monitors from file(s)
- [ ] Add Single monitor from `inline` data
- [ ] Delete Single Monitor by name
- [x] Supported Monitor types (tested)
  - [x] HTTP
  - [x] JSON_QUERY
  - [x] PING

### Status Page

- [x] List all `staus page`(s)
- [x] See details of a `single status page`
- [x] Add a new `status page`.
- [ ] Add status pages from file(s)
