# Monitors

`kumaone`'s primary objective is to enable user to add `monitor`(s) in bulk. `kumaone` uses `yaml` file to determine
monitor configuration and create them. Here is an example monitor config.

```yaml
---
monitors:
  google:
    - name: Google
      type: http
      url: https://google.com
    - name: Gmail
      type: http
      url: https://mail.google.com
```

In the above code snippet, we can see a few components.

```yaml
---
monitors:
```
Here `monitors` is the **keyword**, this let's `kumaone` know that we are instructing to create monitors.

Next, we have `google:`

```yaml
---
monitors:
  google:
```

This will instruct `kumaone` to create a `monitor` of type `group`. Each group can have a list of monitors.

```{seealso}
A group named `default` will instruct `kumaone` to add the following list of monitors at the root of the monitor path.
```

```{warning}
Group name can NOT be same as one of the monitors in the list. In above example `group` name is `google` and first
monitor in the group is named `Google`. (Notice the difference in the capital letter).
```
## Supported monitors

```{attention}
Following monitors are supported (tested) by **`kumaone`** NOT `uptime kuma`. To see a full list of monitor type
supported for `uptime kuma` [documentation](https://github.com/louislam/uptime-kuma/wiki/).
```

- GROUP
- HTTP
- JSON_QUERY
- PING

```{seealso}
More monitors types will be added to `kumaone` in the future.
```

## Add monitors

To add one or more monitors we can provide monitor configurations via one single file or in multiple files via
`--monitors` or `-m` option.

### Single file

```shell
kumaone monitor add -m examples/monitor.config.example.yaml
```

```text
$ kumaone monitor add -m examples/monitor.config.example.yaml
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📋 Checking input data path.
🔆 Single file input detected. Input file: 'examples/monitor.config.example.yaml'.
-------------------------------------- GOOGLE ----------------------------------
🌻 Monitor group 'google' already exists.
🌻 Monitor process 'Google' already exists.
🌻 Monitor process 'Gmail' already exists.
-------------------------------------- HOMELAB ---------------------------------
🌻 Monitor group 'homelab' already exists.
🌻 Monitor process 'PI Server' already exists.
🌻 Monitor process 'Windows Desktop' already exists.
-------------------------------------- DEFAULT ---------------------------------
🐣 Monitor process for 'Personal Website' has been created.
🌻 Monitor process 'MacBook Pro' already exists.
--------------------------------------------------------------------------------
🧨 Disconnected from server.
```

### Multiple file

```shell
kumaone monitor add -m examples/monitors
```

```text
$ kumaone monitor add -m examples/monitors
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📋 Checking input data path.
📁 Directory input detected. Input file directory: 'examples/monitors'.
💡 '.sh' file type is not supported. Skipping 'ignoreme.sh'.
🔆 3 files found in supported format.
-------------------------------------- DEFAULT ---------------------------------
🌻 Monitor process 'Personal Website' already exists.
🌻 Monitor process 'MacBook Pro' already exists.
-------------------------------------- GOOGLE ----------------------------------
🌻 Monitor group 'google' already exists.
🌻 Monitor process 'Google' already exists.
🌻 Monitor process 'Gmail' already exists.
-------------------------------------- HOMELAB ---------------------------------
🌻 Monitor group 'homelab' already exists.
🌻 Monitor process 'PI Server' already exists.
🌻 Monitor process 'Windows Desktop' already exists.
--------------------------------------------------------------------------------
🧨 Disconnected from server.
```

## Delete monitors

Deleting monitor is as simple as adding them. Monitors can be deleted by providing the same config file or files that
were provided when creating them with `--monitors` or `-m` flag.

```shell
kumaone monitor delete -m examples/monitors/homelab.yaml
```

```text
$ kumaone monitor delete -m examples/monitors/homelab.yaml
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📋 Checking input data path.
🔆 Single file input detected. Input file: 'examples/monitors/homelab.yaml'.
-------------------------------------- HOMELAB ---------------------------------
👻 'PI Server' monitor deletion successful!
👻 'Windows Desktop' monitor deletion successful!
👻 'homelab' monitor deletion successful!
--------------------------------------------------------------------------------
🧨 Disconnected from server.
```

Also, a monitor can be deleted by name.

```shell
kumaone monitor delete --name "MacBook Pro"
```

```text
$ kumaone monitor delete --name "MacBook Pro"
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
👻 'MacBook Pro' monitor deletion successful!
🧨 Disconnected from server.
```

```{note}
Name of the monitor should match with the provided name in the CLI. Monitor names are case sensitive.
```

```{seealso}
Deleting monitor by `id` is not yet implemented.
```

## List monitors

User can list all the monitors available with `list` command. List command take `--groups` and `--processes` option to
list monitor groups and processes separately with their respective uptime kuma monitor id.

```shell
kumaone monitor list
```

```text
$ kumaone monitor list
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
🍔 Available monitors (groups and processes).
Gmail                       google       Google       homelab       MacBook Pro          Personal Website             PI Server        pi-prime
Windows Desktop
🧨 Disconnected from server.
```

Only list the groups or processes

```shell
kumaone monitor list --processes
```

```text
$ kumaone monitor list --processes
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
🍔 Available monitor processes.
┏━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ id  ┃ name             ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ 16  │ pi-prime         │
│ 192 │ Google           │
│ 193 │ Gmail            │
│ 205 │ Personal Website │
│ 209 │ MacBook Pro      │
│ 211 │ PI Server        │
│ 212 │ Windows Desktop  │
└─────┴──────────────────┘
🧨 Disconnected from server.
```

## Show monitor

User can get details about a `single` monitor by id. User can easily get uptime kuma monitor id form
above command (`kumaone monitor list --processes`).

```shell
kumaone monitor show --id 192
```

```text
kumaone monitor show --id 192
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
🧁 Details about monitor 'Google'
{
    "accepted_statuscodes": [
        "200-299"
    ],
    "active": true,
    "authDomain": null,
    "authMethod": "",
    "authWorkstation": null,
    "basic_auth_pass": null,
    "basic_auth_user": null,
    "body": null,
    "childrenIDs": [],
    "databaseConnectionString": null,
    "databaseQuery": null,
    "description": null,
    "dns_last_result": null,
    "dns_resolve_server": null,
    "dns_resolve_type": null,
    "docker_container": null,
    "docker_host": null,
    "expectedValue": null,
    "expiryNotification": false,
    "forceInactive": false,
    "game": null,
    "gamedigGivenPortOnly": true,
    "grpcBody": null,
    "grpcEnableTls": false,
    "grpcMetadata": null,
    "grpcMethod": null,
    "grpcProtobuf": null,
    "grpcServiceName": null,
    "grpcUrl": null,
    "headers": null,
    "hostname": null,
    "httpBodyEncoding": "json",
    "id": 192,
    "ignoreTls": false,
    "includeSensitiveData": true,
    "interval": 60,
    "invertKeyword": false,
    "jsonPath": null,
    "kafkaProducerAllowAutoTopicCreation": false,
    "kafkaProducerBrokers": null,
    "kafkaProducerMessage": null,
    "kafkaProducerSaslOptions": null,
    "kafkaProducerSsl": false,
    "kafkaProducerTopic": null,
    "keyword": null,
    "maintenance": false,
    "maxredirects": 10,
    "maxretries": 1,
    "method": "GET",
    "mqttPassword": null,
    "mqttSuccessMessage": null,
    "mqttTopic": null,
    "mqttUsername": null,
    "name": "Google",
    "notificationIDList": {},
    "oauth_auth_method": null,
    "oauth_client_id": null,
    "oauth_client_secret": null,
    "oauth_scopes": null,
    "oauth_token_url": null,
    "packetSize": 56,
    "parent": 53,
    "pathName": "google / Google",
    "port": null,
    "proxyId": null,
    "pushToken": null,
    "radiusCalledStationId": null,
    "radiusCallingStationId": null,
    "radiusPassword": null,
    "radiusSecret": null,
    "radiusUsername": null,
    "resendInterval": 0,
    "retryInterval": 60,
    "screenshot": null,
    "tags": [],
    "timeout": 48,
    "tlsCa": null,
    "tlsCert": null,
    "tlsKey": null,
    "type": "http",
    "upsideDown": false,
    "url": "https://google.com",
    "weight": 2000
}
🧨 Disconnected from server.
```
