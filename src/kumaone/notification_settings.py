#!/usr/bin/env python3

"""Notification settings module for kumaone"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

notification_providers = {
    "discord": {
        "discordWebhookUrl": "",
        "discordUsername": "",
        "discordPrefixMessage": "",
    },
    "opsgenie": {
        "opsgenieRegion": "",
        "opsgenieApiKey": "",
        "opsgeniePriority": "",
    },
    "pagerduty": {
        "pagerdutyIntegrationKey": "",
        "pagerdutyPriority": "",
        "pagerdutyIntegrationUrl": "",
        "pagerdutyAutoResolve": "",
    },
    "rocket.chat": {
        "rocketwebhookURL": "",
        "rocketchannel": "",
        "rocketusername": "",
        "rocketiconemo": "",
    },
    "slack": {
        "slackwebhookURL": "",
        "slackchannelnotify": "",
        "slackchannel": "",
        "slackusername": "",
        "slackiconemo": "",
    },
    "smtp": {
        "smtpFrom": "",
        "smtpTo": "",
        "smtpHost": "",
        "smtpPort": "",
        "smtpSecure": "",
        "smtpIgnoreTLSError": "",
        "smtpDkimDomain": "",
        "smtpDkimKeySelector": "",
        "smtpDkimPrivateKey": "",
        "smtpDkimHashAlgo": "",
        "smtpDkimheaderFieldNames": "",
        "smtpDkimskipFields": "",
        "smtpUsername": "",
        "smtpPassword": "",
        "customSubject": "",
        "smtpCC": "",
        "smtpBCC": "",
    },
    "teams": {
        "webhookUrl": "",
    },
    "webhook": {
        "webhookContentType": "",
        "webhookCustomBody": "",
        "webhookAdditionalHeaders": "",
        "webhookURL": "",
    },
}
