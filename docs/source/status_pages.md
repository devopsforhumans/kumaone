# Status pages

`kumaone` enables user to create status pages form `single` file or `multiple` files. `kumaone` also helps
users to assign certain monitors to the status page via `yaml` formatted file. Usually, `kumaon` expects
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

`status_pages` is a list of status pages that should be added. `Uptime Kuma` status pages are added and then
the corresponding `monitors` are attached to the `status page` and `saved`. `kumaone` does all of that in single
command.

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
