# Status pages

`kumaone` enables user to create status pages form `single` file or `multiple` files. `kumaone` also helps
users to assign certain monitors to the status page via `yaml` formatted file. Usually, `kumaone` expects
status page configuration in the same file as monitors with `status_pages` stanza.

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
status_pages:
  - title: Google Status
    slug: google
    description: "Google services status page."
    theme: "auto"
    published: True
    showTags: False
    domainNameList: ["google.uptimestatus.do"]
    googleAnalyticsId: ""
    customCSS: ""
    footerText: "this goes in the footer of status page"
    showPoweredBy: False
    showCertificateExpiry: True
    icon: "/icon.svg"
    publicGroupList:
      - name: Services
        weight: 1
        monitorList:
          - Google
          - Gmail
```

`status_pages` is a list of status pages that should be added.

## Add and save status page

`Uptime Kuma` status pages are added and then the corresponding `monitors` are attached to the `status page` and
`saved`. `kumaone` does all of that in single command.

```shell
kumaone status-page add -p examples/monitors --save
```

```text
$ kumaone status-page add -p examples/monitors --save
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📋 Checking input data path.
📁 Directory input detected. Input file directory: 'examples/monitors'.
💡 '.sh' file type is not supported. Skipping 'ignoreme.sh'.
🔆 2 files found in supported format.
🐣 Status page 'Google Status (google)' has been created.
💾 Status page saved successfully!
🐣 Status page 'Homelab Status Page (homelab)' has been created.
💾 Status page saved successfully!
🧨 Disconnected from server.
```

If `--save` command is not provided, `kumaone` will only create the status page. Monitors won't be added to the status
page.

```{important}
To add the monitors to the status page, add `--save` option.
```

A status page can also be added (not saved -> no monitor attached to it) with proving a `title` and `slug`.

```shell
kumaone status-page add --title "Test Status Page" --slug "test23"
```

```text
$ kumaone status-page add --title "Test Status Page" --slug "test23"
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
🐣 Status page 'Test Status Page (test23)' has been created.
🧨 Disconnected from server.
```

## Delete status page

Status page can be deleted via `slug` (one at a time) or providing `--pages` one or multiple files. Deleting status
page(s) works similar as adding a status page.

Delete an existing status page by `slug`.

```shell
kumaone status-page delete --slug "test23"
```

```text
kumaone status-page delete --slug "test23"
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
🗑 Status page 'test23' has been deleted.
🧨 Disconnected from server.
```

Status page(s) can be deleted by providing status page configuration file as an argument to `--pages` option.

```shell
kumaone status-page delete --pages examples/monitors/homelab.yaml
```

```text
$ kumaone status-page delete --pages examples/monitors/homelab.yaml
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📋 Checking input data path.
🔆 Single file input detected. Input file: 'examples/monitors/homelab.yaml'.
🗑 Status page 'homelab' has been deleted.
🧨 Disconnected from server.
```

Deletion of status pages also works with multiple files (directory input).

```shell
kumaone status-page delete --pages examples/monitors
```

```text
$ kumaone status-page delete --pages examples/monitors
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📋 Checking input data path.
📁 Directory input detected. Input file directory: 'examples/monitors'.
💡 '.sh' file type is not supported. Skipping 'ignoreme.sh'.
🔆 2 files found in supported format.
🗑 Status page 'google' has been deleted.
🟠 Status page 'homelab' does not exist.
🧨 Disconnected from server.
```

## List status pages

`list` sub-command for `status-pages` shows all the status pages available.

```shell
kumaone status-page list
```

```text
$ kumaone status-page list
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
🍔 Available status pages.
┏━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ id ┃ slug     ┃ Title               ┃
┡━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ dalwar23 │ Personal WebPage    │
│ 52 │ google   │ Google Status       │
│ 53 │ homelab  │ Homelab Status Page │
└────┴──────────┴─────────────────────┘
🧨 Disconnected from server.
```

## Show status page details

Users can find out details about any status page with the status page `slug`.

```shell
kumaone status-page show --slug google
```

```text
kumaone status-page show --slug google
🥳 Uptime kuma config file found at: /Users/dalwar23/.config/kumaone/kuma.yaml
🥨 Connected to http://uptime.homelab.do
🔐 Successfully logged in.
📄 'google' status page details
{
    "customCSS": "",
    "description": "Google services status page.",
    "domainNameList": [
        "google.uptimestatus.do"
    ],
    "footerText": "this goes in the footer of status page",
    "googleAnalyticsId": "",
    "icon": "/icon.svg",
    "id": 52,
    "incident": null,
    "maintenanceList": [],
    "publicGroupList": [
        {
            "id": 62,
            "monitorList": [
                {
                    "certExpiryDaysRemaining": 43,
                    "id": 192,
                    "name": "Google",
                    "sendUrl": 0,
                    "type": "http",
                    "validCert": true
                },
                {
                    "certExpiryDaysRemaining": 43,
                    "id": 193,
                    "name": "Gmail",
                    "sendUrl": 0,
                    "type": "http",
                    "validCert": true
                }
            ],
            "name": "Services",
            "weight": 1
        }
    ],
    "published": true,
    "showCertificateExpiry": true,
    "showPoweredBy": false,
    "showTags": false,
    "slug": "google",
    "theme": "auto",
    "title": "Google Status"
}
🧨 Disconnected from server.
```
