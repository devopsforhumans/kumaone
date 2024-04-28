#!/usr/bin/env python3

"""Notification settings module for kumaone"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

notification_types = {
    "discord": "discord",
    "email": "smtp",
    "opsgenie": "Opsgenie",
    "pagerduty": "PagerDuty",
    "rocketchat": "rocket.chat",
    "slack": "slack",
    "teams": "teams",
    "webhook": "webhook",
}

notification_providers = {
    "discord": {
        "discordWebhookUrl": {"required": True},
        "discordUsername": {"required": False},
        "discordPrefixMessage": {"required": False},
    },
    "opsgenie": {
        "opsgenieRegion": {"required": True},
        "opsgenieApiKey": {"required": True},
        "opsgeniePriority": {"required": False},
    },
    "pagerduty": {
        "pagerdutyIntegrationKey": {"required": True},
        "pagerdutyPriority": {"required": False},
        "pagerdutyIntegrationUrl": {"required": False},
        "pagerdutyAutoResolve": {"required": False},
    },
    "rocketchat": {
        "rocketwebhookURL": {"required": True},
        "rocketchannel": {"required": False},
        "rocketusername": {"required": False},
        "rocketiconemo": {"required": False},
    },
    "slack": {
        "slackwebhookURL": {"required": True},
        "slackchannelnotify": {"required": False},
        "slackchannel": {"required": False},
        "slackusername": {"required": False},
        "slackiconemo": {"required": False},
    },
    "email": {
        "smtpFrom": {"required": True},
        "smtpTo": {"required": True},
        "smtpHost": {"required": True},
        "smtpPort": {"required": True},
        "smtpSecure": {"required": False},
        "smtpIgnoreTLSError": {"required": False},
        "smtpDkimDomain": {"required": False},
        "smtpDkimKeySelector": {"required": False},
        "smtpDkimPrivateKey": {"required": False},
        "smtpDkimHashAlgo": {"required": False},
        "smtpDkimheaderFieldNames": {"required": False},
        "smtpDkimskipFields": {"required": False},
        "smtpUsername": {"required": False},
        "smtpPassword": {"required": False},
        "customSubject": {"required": False},
        "smtpCC": {"required": False},
        "smtpBCC": {"required": False},
    },
    "teams": {
        "webhookUrl": {"required": True},
    },
    "webhook": {
        "webhookURL": {"required": True},
        "webhookContentType": {"required": True},
        "webhookCustomBody": {"required": False},
        "webhookAdditionalHeaders": {"required": False},
    },
}
