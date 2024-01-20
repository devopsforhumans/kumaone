#!/usr/bin/env python3

"""Payload handler module for kumaone"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
from rich.console import Console

# Import custom (local) python packages
from .notification_settings import notification_providers
from .settings import authentication_methods

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar23@pm.me"

console = Console()


def _get_monitor_payload(
    type=None,
    name=None,
    parent=None,
    description=None,
    interval=60,
    retryInterval=60,
    resendInterval=0,
    maxretries=1,
    upsideDown=False,
    notificationIDList=None,
    httpBodyEncoding="json",
    # HTTP, KEYWORD, JSON_QUERY, REAL_BROWSER
    url=None,
    # HTTP, KEYWORD, GRPC_KEYWORD
    maxredirects=10,
    accepted_statuscodes=None,
    # HTTP, KEYWORD, JSON_QUERY
    expiryNotification=False,
    ignoreTls=False,
    proxyId=None,
    method="GET",
    body=None,
    headers=None,
    authMethod="",
    tlsCert=None,
    tlsKey=None,
    tlsCa=None,
    basic_auth_user=None,
    basic_auth_pass=None,
    authDomain=None,
    authWorkstation=None,
    oauth_auth_method="client_secret_basic",
    oauth_token_url=None,
    oauth_client_id=None,
    oauth_client_secret=None,
    oauth_scopes=None,
    timeout=48,
    # KEYWORD
    keyword=None,
    invertKeyword=False,
    # GRPC_KEYWORD
    grpcUrl=None,
    grpcEnableTls=False,
    grpcServiceName=None,
    grpcMethod=None,
    grpcProtobuf=None,
    grpcBody=None,
    grpcMetadata=None,
    # PORT, PING, DNS, STEAM, MQTT, RADIUS, TAILSCALE_PING
    hostname=None,
    # PING
    packetSize=56,
    # PORT, DNS, STEAM, MQTT, RADIUS
    port=None,
    # DNS
    dns_resolve_server="1.1.1.1",
    dns_resolve_type="A",
    # MQTT
    mqttUsername="",
    mqttPassword="",
    mqttTopic="",
    mqttSuccessMessage="",
    # SQLSERVER, POSTGRES, MYSQL, MONGODB, REDIS
    databaseConnectionString=None,
    # SQLSERVER, POSTGRES, MYSQL
    databaseQuery=None,
    # DOCKER
    docker_container="",
    docker_host=None,
    # RADIUS
    radiusUsername=None,
    radiusPassword=None,
    radiusSecret=None,
    radiusCalledStationId=None,
    radiusCallingStationId=None,
    # GAMEDIG
    game=None,
    gamedigGivenPortOnly=True,
    # JSON_QUERY
    jsonPath=None,
    expectedValue=None,
    # KAFKA_PRODUCER
    kafkaProducerBrokers=None,
    kafkaProducerTopic=None,
    kafkaProducerMessage=None,
    kafkaProducerSsl=False,
    kafkaProducerAllowAutoTopicCreation=False,
    kafkaProducerSaslOptions=None,
):
    """
    Generates payload for monitor "add" event

    :return: (dict) Python dictionary for payload
    """

    if accepted_statuscodes is None:
        accepted_statuscodes = ["200-299"]

    if notificationIDList is None:
        notificationIDList = []

    monitor_data = {
        "type": type,
        "name": name,
        "interval": interval,
        "retryInterval": retryInterval,
        "maxretries": maxretries,
        "notificationIDList": notificationIDList,
        "upsideDown": upsideDown,
        "resendInterval": resendInterval,
        "description": description,
        "httpBodyEncoding": httpBodyEncoding,
        "parent": parent,
        "expiryNotification": expiryNotification,
        "ignoreTls": ignoreTls,
        "proxyId": proxyId,
        "method": method,
        "body": body,
        "headers": headers,
        "authMethod": authMethod,
        "timeout": timeout,
    }

    # HTTP, KEYWORD, JSON_QUERY, REAL_BROWSER
    monitor_data.update({"url": url})

    if type in ["keyword", "grpc-keyword"]:
        monitor_data.update(
            {
                "keyword": keyword,
                "invertKeyword": invertKeyword,
            }
        )

    # HTTP, KEYWORD, GRPC_KEYWORD
    monitor_data.update(
        {
            "maxredirects": maxredirects,
            "accepted_statuscodes": accepted_statuscodes,
        }
    )

    # AUTH METHODS
    if authMethod:
        if authMethod in authentication_methods:
            if authMethod in ["basic", "ntlm"]:
                monitor_data.update(
                    {
                        "basic_auth_user": basic_auth_user,
                        "basic_auth_pass": basic_auth_pass,
                    }
                )

            if authMethod == "ntlm":
                monitor_data.update(
                    {
                        "authDomain": authDomain,
                        "authWorkstation": authWorkstation,
                    }
                )

            if authMethod == "mtls":
                monitor_data.update(
                    {
                        "tlsCert": tlsCert,
                        "tlsKey": tlsKey,
                        "tlsCa": tlsCa,
                    }
                )

            if authMethod == "oauth2-cc":
                monitor_data.update(
                    {
                        "oauth_auth_method": oauth_auth_method,
                        "oauth_token_url": oauth_token_url,
                        "oauth_client_id": oauth_client_id,
                        "oauth_client_secret": oauth_client_secret,
                        "oauth_scopes": oauth_scopes,
                    }
                )
        else:
            console.print(
                f":blowfish: Provided authentication method: {authMethod} is not supported.", style="logging.level.info"
            )

    if type == "grpc-keyword":
        monitor_data.update(
            {
                "grpcUrl": grpcUrl,
                "grpcEnableTls": grpcEnableTls,
                "grpcServiceName": grpcServiceName,
                "grpcMethod": grpcMethod,
                "grpcProtobuf": grpcProtobuf,
                "grpcBody": grpcBody,
                "grpcMetadata": grpcMetadata,
            }
        )

    # DNS, MQTT, PING, PORT, RADIUS, STEAM, TAILSCALE_PING
    if type in ["dns", "mqtt", "ping", "port", "radius", "steam", "tailscale-ping"]:
        monitor_data.update(
            {
                "hostname": hostname,
            }
        )

    # PING
    if type == "ping":
        monitor_data.update(
            {
                "packetSize": packetSize,
            }
        )

    # PORT, DNS, STEAM, MQTT, RADIUS
    if not port:
        if type == "radius":
            port = 1812
    monitor_data.update(
        {
            "port": port,
        }
    )

    # DNS
    if type == "dns":
        monitor_data.update(
            {
                "dns_resolve_server": dns_resolve_server,
                "dns_resolve_type": dns_resolve_type,
            }
        )
        if not port:
            monitor_data.update({"port": 53})

    # MQTT
    if type == "mqtt":
        monitor_data.update(
            {
                "mqttUsername": mqttUsername,
                "mqttPassword": mqttPassword,
                "mqttTopic": mqttTopic,
                "mqttSuccessMessage": mqttSuccessMessage,
            }
        )

    # SQLSERVER, POSTGRES, MYSQL, MONGODB, REDIS
    if type in ["sqlserver", "postgres", "mysql", "mongodb", "redis"]:
        monitor_data.update({"databaseConnectionString": databaseConnectionString})

    # SQLSERVER, POSTGRES, MYSQL
    if type in ["sqlserver", "postgres", "mysql"]:
        monitor_data.update(
            {
                "databaseQuery": databaseQuery,
            }
        )

    # DOCKER
    if type == "docker":
        monitor_data.update(
            {
                "docker_container": docker_container,
                "docker_host": docker_host,
            }
        )

    # RADIUS
    if type == "radius":
        monitor_data.update(
            {
                "radiusUsername": radiusUsername,
                "radiusPassword": radiusPassword,
                "radiusSecret": radiusSecret,
                "radiusCalledStationId": radiusCalledStationId,
                "radiusCallingStationId": radiusCallingStationId,
            }
        )

    # GAMEDIG
    if type == "gamedig":
        monitor_data.update(
            {
                "game": game,
                "gamedigGivenPortOnly": gamedigGivenPortOnly,
            }
        )

    # JSON_QUERY
    if type == "json-query":
        monitor_data.update(
            {
                "jsonPath": jsonPath,
                "expectedValue": expectedValue,
            }
        )

    # KAFKA_PRODUCER
    if type == "kafka-producer":
        if kafkaProducerBrokers is None:
            kafkaProducerBrokers = []
        if not kafkaProducerSaslOptions:
            kafkaProducerSaslOptions = {
                "mechanism": "None",
            }
        monitor_data.update(
            {
                "kafkaProducerBrokers": kafkaProducerBrokers,
                "kafkaProducerTopic": kafkaProducerTopic,
                "kafkaProducerMessage": kafkaProducerMessage,
                "kafkaProducerSsl": kafkaProducerSsl,
                "kafkaProducerAllowAutoTopicCreation": kafkaProducerAllowAutoTopicCreation,
                "kafkaProducerSaslOptions": kafkaProducerSaslOptions,
            }
        )

    return monitor_data


def _get_status_page_data_payload(
    slug=None,
    id=None,
    title=None,
    description=None,
    theme="auto",
    published=True,
    showTags=False,
    domainNameList=None,
    googleAnalyticsId=None,
    customCSS="",
    footerText=None,
    showPoweredBy=False,
    showCertificateExpiry=False,
    icon="/icon.svg",
    publicGroupList=None,
):
    """
    Generates payload data for status page "save" event

    :param slug: (str) Status page slug.
    :param id: (int) Status page ID.
    :param title: (str) Status page title.
    :param description: (str) Status page description.
    :param theme: (str) Status page theme. [auto], light, or dark theme.
    :param published: (bool) Status page status. Default [True].
    :param showTags: (bool) Should the tags be visible on the page. Default [False].
    :param domainNameList: (list) List of domain names.
    :param googleAnalyticsId: (str) Google Analytics ID.
    :param customCSS: (str) Custom CSS.
    :param footerText: (str) Footer text for status page.
    :param showPoweredBy: (bool) Show powered by. Default [False].
    :param showCertificateExpiry: (bool) Show the status page show SSL certificate expiry time.
    :param icon: (str) Status page icon location path. Default ["/icon.svg"]
    :param publicGroupList: (list) List of public groups.
    :return: (dict) Status page save payload data
    """

    if not domainNameList:
        domainNameList = []
    if not publicGroupList:
        publicGroupList = []

    status_page_payload = {
        "id": id,
        "slug": slug,
        "title": title,
        "description": description,
        "domainNameList": domainNameList,
        "icon": icon,
        "theme": theme,
        "published": published,
        "showTags": showTags,
        "showPoweredBy": showPoweredBy,
        "googleAnalyticsId": googleAnalyticsId,
        "customCSS": customCSS,
        "footerText": footerText,
        "showCertificateExpiry": showCertificateExpiry,
    }

    return slug, status_page_payload, icon, publicGroupList
