# Installation

kumaone (`kumaone`) requires Python 3.8 or above. If you do not already have a
Python environment configured on your computer, please see the
[Python](https://www.python.org) page for instructions on installing Python
environment.

Assuming that the default python environment is already configured on your computer, and
you intend to install `kumaone` in it, to create and work with Python virtual
environments, please follow instructions from [pipenv](https://pipenv.pypa.io/en/latest/).

To start the installation process, please make sure the latest version of `pip`
(python3 package manager) is installed. If `pip` is not installed, please refer to
the [Pip documentation](https://pip.pypa.io/en/stable/installing/) and install
`pip` first.

## Linux/macOS

Install the latest release of `kumaone` with ``pip``:

```shell
pip install kumaone
```

To upgrade to a newer version use the `--upgrade` flag:

```shell
pip install --upgrade kumaone
```

If system-wide installation is not possible for permission reasons, use `--user`
flag to install `kumaone` for current user

```shell
pip install --user kumaone
```

## Windows

Considering `python3` is installed and `pip` is configured.

Open Cmder/ConEmu and Type:

```shell
pip install kumaone
```

Or if the `pipenv shell` is active

```shell
pipenv install kumaone
```

This should install `kumaone` with all the required dependencies.

## Install from Source

Alternatively, `kumaone` can be installed manually by downloading the current version
from [GitHub](https://github.com/dalwar23/kumaone) or
[PyPI](https://pypi.org/project/kumaone/). To install a downloaded versions, please
unpack it in a preferred directory and run the following command at the top level of
the directory:

```shell
pip install .
```

## Dependencies

This package requires a configuration file in ``.yaml`` format. The
look-up priority for the configuration file is as following-

1. `<user_home_directory>/.config/kumaone/kuma.yaml` (`Window/Linux/MacOS`) [**Default**]
2. `<user_home_directory>/kuma.yaml` (`Windows/Linux/MacOS`)
3. `<current_working_directory>/kuma.yaml` (`Windows/Linux/MacOS`)
4. `/etc/<package_name>/kuma.yaml` (`Linux/MacOS`)

If `kuma.yaml` doesn't exists in one of these locations, the program will prompt for creating
a new config. Alternatively you can provide a custom location for `kumaone` config. Find out more
with

```shell
kumaone config create --help
```

```{tip}
It's recommended to leave the config file creation at one of the location above. This way while using `kumaone`,
user doesn't have to provide custom config path everytime with `-c` or `--config` flag.
```

### Windows

Windows system, by default doesn't allow creation of `.` prefixed directory from GUI,
so use the following -

- Open `cmd` and change the directory to the ``home`` folder of the user
- Run ``mkdir .config`` (if the folder doesn't exist)
- Run ``cd .config``
- Run ``mkdir kumaone``

Now that the ``.`` prefixed directory is created use the following command to create the config
file.

```shell
kumaone config create
```

### Linux/MacOS

```shell
kumaone config create
```

```{note}
Example config files can be found under examples directory in `kumaone` GitHub repository.
```
