# User Guide

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

```{toctree}
:maxdepth: 2

monitors.md
status_pages.md
```
