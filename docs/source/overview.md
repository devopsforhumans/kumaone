# Overview

`kumaone` is a python based CLI tool to interact with `uptime kuma` server. [Uptime Kuma](https://uptime.kuma.pet/) is
an easy-to-use self-hosted monitoring tool.

## Main features

- `kumaone` enables user to interact with uptime kuma server to create/delete monitor, notification, statuspage in
  **bulk**.
- `kumaone` can handle `single file` or `multiple file` input for creating/deleting `monitor` and `status pages`.
- `kumaone` can also create/delete multiple `notification` provider.


## kumaone

```shell

$ kumaone --help

 Usage: kumaone [OPTIONS] COMMAND [ARGS]...

 Mission control for kumaone, an uptime kuma helper python package.

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --log-level                 TEXT  Set log level. [default: NOTSET]                                                                          │
│ --install-completion              Install completion for the current shell.                                                                 │
│ --show-completion                 Show completion for the current shell, to copy it or customize the installation.                          │
│ --help                            Show this message and exit.                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ config             Kumaone configuration manager.                                                                                           │
│ info               Show information about kumaone application.                                                                              │
│ monitor            Kumaone monitor manager. An uptime kuma monitor group and process monitor manager wrapper.                               │
│ notification       Kumaone notification process manager. An uptime kuma notification processes manager wrapper.                             │
│ status-page        Kumaone status page manager. An uptime kuma status page manager wrapper.                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
