# Notifications

There are quite a few notification providers supported by `uptime kuma`. In practice, we use notification provider to
get notified about events and most of the time we use one or two notification providers. It is by design of `kumaone`
the configuration of the notification providers are sources from a separate file or files, unlike monitors and status
pages.

This gives the users flexibility to use same providers for multiple process monitors and events.

Example configuration of `notificaiton` provider config file

```yaml
---
notifications:
  - rocketchat:
      name: "Uptime notification"
      type: "rocket.chat"
      is_default: false
      apply_existing: false
      rocketwebhookURL: "https://chat.homelab.do"
      rocketiconemo: "rocket"
      rocketusername: "bot"
      rocketchannel: "somechannel"
```

```{hint}
Currently each of the notificaiton provider has it's own required parameters and `kumaone` doesn't have any CLI
commands to expose them to the user. This feature is planned but not yet implemented. See `examples` directory in
`GitHub` for references.
```

## Supported notification providers

```{attention}
Following notification providers are supported by **`kumaone`** NOT `uptime kuma`. To see a full list of provider
support for `uptime kuma` [please see here](https://github.com/louislam/uptime-kuma/wiki/Notification-Methods).
```

- MS Teams
- Rocket.Chat
- Slack
- Webhook

```{seealso}
More notification providers will be added to `kumaone` in the future.
```

## Add notification

To add notification(s), use `add` subcommand with `notifications` command. To provide the notification config file
use `--notifications` or `-n` option with file path as argument.

```shell
kumaone notifications add --notifications examples/notification.config.example.yaml
```

```text
$ kumaone notification add --notifications examples/notification.config.example.yaml
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
💾 Notification provider 'rocket.chat' added successfully.
💾 Notification provider 'slack' added successfully.
💾 Notification provider 'teams' added successfully.
💾 Notification provider 'webhook' added successfully.
🧨 Disconnected from server.
```

## Delete notification

Deleting notification is as easy as adding them. Provide the notification config file path to `delete` sub command with
`--notifications` option.

```shell
kumaone notification delete --notifications examples/notification.config.example.yaml
```

```text
$ kumaone notification delete --notifications examples/notification.config.example.yaml
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
👻 Notification provider with id: '27' has been deleted.
👻 Notification provider with id: '28' has been deleted.
👻 Notification provider with id: '29' has been deleted.
👻 Notification provider with id: '30' has been deleted.
🧨 Disconnected from server.
```

User can also delete notifications by notification `title` or notification `id`.

```shell
kumaone notification delete --id 32
```

or


```shell
kumaone notification delete --title "Uptime slack notification"
```

```text
$ kumaone notification delete --title "Uptime slack notification"
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
👻 Notification provider with id: '32' has been deleted.
🧨 Disconnected from server.
```

## List notification

To list all available `notification` provider configuration, `list` sub-command can be used.

```shell
kumaone notification list
```

```text
$ kumaone notification list
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📣 Available notification providers
┏━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
┃ id ┃ type        ┃ title                       ┃ active ┃ isDefault ┃
┡━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
│ 31 │ rocket.chat │ Uptime notification         │ True   │ False     │
│ 32 │ slack       │ Uptime slack notification   │ True   │ False     │
│ 33 │ teams       │ Uptime teams notification   │ True   │ False     │
│ 34 │ webhook     │ Uptime webhook notification │ True   │ False     │
└────┴─────────────┴─────────────────────────────┴────────┴───────────┘
🧨 Disconnected from server.
```

## Show notification details

To see details about a specific notification provider, `show` sub-command can be used.

```shell
kumaone notification show --id 31
```

```text
kumaone notification show --id 31
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📣 Available notification providers
┏━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
┃ id ┃ type        ┃ title               ┃ active ┃ isDefault ┃
┡━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
│ 31 │ rocket.chat │ Uptime notification │ True   │ False     │
└────┴─────────────┴─────────────────────┴────────┴───────────┘
🧨 Disconnected from server.
```

`--verbose` option flag can help get more details about a specific notification provider.

```shell
kumaone notification show --id 31 --verbose
```

```text
kumaone notification show --id 31 --verbose
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📣 Available notification providers
[
    {
        "active": true,
        "apply_existing": false,
        "id": 31,
        "isDefault": false,
        "is_default": false,
        "name": "Uptime notification",
        "rocketchannel": "somechannel",
        "rocketiconemo": "rocket",
        "rocketusername": "bot",
        "rocketwebhookURL": "https://chat.homelab.do",
        "type": "rocket.chat",
        "userId": 1
    }
]
🧨 Disconnected from server.
```
