# kumaone

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![PyPI - Version](https://img.shields.io/pypi/v/kumaone.svg)](https://pypi.org/project/kumaone)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kumaone.svg)](https://pypi.org/project/kumaone)
[![Documentation Status](https://readthedocs.org/projects/kumaone/badge/?version=latest)](https://kumaone.readthedocs.io/en/latest/?badge=latest)

-----

**Table of Contents**

- [Note](#note)
- [Virtualenv](#virtualenv)
- [Installation](#installation)

## Note

`kumaone`'s primary objective is to enable users to perform bulk action in `uptime kuma` server. A very special thanks
to the author and contributors of the project [uptime-kuma-api](https://github.com/lucasheld/uptime-kuma-api). `kumaone`
is built by studying and understanding the code of `uptime-kuma-api` and in places I used some parts of the code as it
is from `uptime-kuma-api`. Appreciate the outstanding work done by the author and contributors of both
[uptime kuma](https://github.com/louislam/uptime-kuma) and `uptime-kuma-api` project.

`kumaone` is a CLI application. Designed for bulk operations mainly from reading configuration files. `kumaone` is very
early in development. Contribution and constructive feedbacks are always welcome.

## Virtualenv

- Install `pipenv` from [here](https://pipenv.pypa.io/en/latest/)

- Activate virtual environment

  ```shell
  pipenv shell
  ```

  > if there are no virtual environment available (e.g. first use), a virtual environment will be created and activated
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

## To Do List

### Info

- [x] Show information about `kumaone`

### Configuration

- [x] Show `uptime kuma` configuration (default/custom paths).
- [x] Create `uptime kuma` configuration (default/custom path).
- [x] Delete `uptime kuma` configuration.
- [ ] Edit `uptime kuma` configuration.

### Monitors

- Supported Monitor types (tested)
  - [x] HTTP
  - [x] JSON_QUERY
  - [x] PING
- [x] List all monitors.
- [x] List monitor by `groups` and `processes` also.
- [x] Show details of a monitor by ID.
- [x] Bulk `add` monitors from file(s).
- [x] Bulk `delete` monitors from file(s).
- [ ] Add single monitor from `inline` dictionary data.
- [x] Delete single Monitor by name.
- [x] Delete single monitor by id.

### Status Page

- [x] List all `staus page`(s).
- [x] See details of a `single status page`.
- [x] Add a new `status page`.
- [x] Add status pages from file(s).
- [x] Delete single status page by slug.
- [x] Delete status page from file(s).

### Notification

- Supported notification providers (tested)
  - [x] Discord
  - [x] Email(SMTP)
  - [x] Opsgenie
  - [x] PagerDuty
  - [x] Rocket.Chat
  - [x] Slack
  - [x] Teams
  - [x] Webhook
- [x] List all `notification`(s).
- [x] See details of a `single notification` by name/id.
- [ ] Add new notification (interactive).
- [x] Add notifications from single file.
- [x] Delete notification by name.
- [x] Delete notification by id.
- [x] Delete notifications from single file.

### Maintenance

TBA

### Incident

TBA

### Change Password

- [ ] Change password from CLI.
- [ ] Update password in `kumaone` config.

### Cleanup

- [ ] Clear heartbeats.
- [ ] Clear statistics.
- [ ] Clear events.

### Backlog

- [ ] Don't stop the program if one monitor process runs into error.
- [ ] Add debug logs for methods.
