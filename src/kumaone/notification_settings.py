#!/usr/bin/env python3

"""Notification settings module for kumaone"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

notification_providers = {
    "rocket.chat": {
        "rocketchannel": "",
        "rocketusername": "",
        "rocketiconemo": "",
        "rocketwebhookURL": "",
    },
    "slack": {
        "slackchannelnotify": "",
        "slackchannel": "",
        "slackusername": "",
        "slackiconemo": "",
        "slackwebhookURL": "",
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
