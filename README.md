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

```console
pip install kumaone
```

## License

`kumaone` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Features

- [x] Show information about `kumaone`
- [x] Show `uptime kuma` configuration (default paths)
- [x] Show `uptime kuma` configuration (custom path)
- [ ] Create `uptime kuma` configuration (default path)
- [ ] Create `uptime kuma` configuration (custom path)
- [ ] Edit `uptime kuma` configuration
- [ ] Delete `uptime kuma` configuration
- [ ] Bulk add monitors
- [ ] Bulk delete monitors
- [ ] Bulk edit monitors
- [ ] Add Single monitor
- [ ] Delete Single Monitor
- [ ] Supported Monitor types
  - [ ] HTTP
  - [ ] JSON_QUERY
  - [ ] PING
  - [ ] PORT
  - [ ] DNS
