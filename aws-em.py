#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from SendEmail import SendEmail
from CreateEmail import CreateEmail
from BuildTable import BuildTable

import datetime
import json
import logging
import sys
import uuid as id
import os

# Set up logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Grab variables from environment
to_email = os.getenv('TO_EMAIL')
from_email = os.getenv('FROM_EMAIL')


def lambda_handler(event, context):

    # Attempt to locate each of the user properties

    #Grab variables from environment
    #to_email = os.getenv['TO_EMAIL']
    #from_email = os.getenv['FROM_EMAIL']

    try:
        user_arn = event['userIdentity']['arn']
    except KeyError as e:
        try:
            user_arn = event['detail']['userIdentity']['arn']
        except KeyError as e:
            user_arn = event['userIdentity']['invokedBy']

    try:
        account_id = event['userIdentity']['accountId']
    except KeyError as e:
        try:
            account_id = event['detail']['userIdentity']['accountId']
        except KeyError as e:
            account_id = event['recipientAccountId']

    try:
        sourceIPAddress = event['sourceIPAddress']
    except KeyError as e:
        sourceIPAddress = event['detail']['sourceIPAddress']

    # Attempt to locate each of the event  properties

    try:
        event_name = event['eventName']
    except KeyError as e:
        event_name = event['detail']['eventName']

    try:
        event_time = event['eventTime']
    except KeyError as e:
        event_time = event['detail']['eventTime']

    try:
        event_type = event['eventType']
    except KeyError as e:
        event_type = event['detail']['eventType']

    # Build custom event object
    custom_event = {
        "user_arn": user_arn,
        "account_id": account_id,
        "sourceIPAddress": sourceIPAddress,
        "event_name": event_name,
        "event_time": event_time,
        "event_type": event_type}

    # Build email subject
    email_subject = str(
        'AWS Event Notification: ' +
        custom_event['event_name'] +
        '-' +
        custom_event['account_id'])

    email = CreateEmail(event, custom_event)
    html = email.make_html('simple.html', event)
    tbuilder = BuildTable(event)
    tbuilder.build()
    send = SendEmail(to=to_email, subject=email_subject, html=html)
    send.send(from_addr=from_email)


if __name__ == '__main__':
    lambda_handler(
        {
            "account": "123456789112",
            "region": "us-east-1",
            "detail": {
                "eventVersion": "1.05",
                "eventID": "f77f9547-3233-4e1d-b247-e404b3924315",
                "eventTime": "2017-09-24T10:35:41Z",
                "additionalEventData": {
                    "MFAUsed": "No",
                    "LoginTo": "https://console.aws.amazon.com/console/home?state=hashArgs%23&isauthcode=true",
                    "MobileVersion": "No"},
                "requestParameters": "None",
                "eventType": "AwsConsoleSignIn",
                "responseElements": {
                    "ConsoleLogin": "Success"},
                "awsRegion": "global",
                "eventName": "ConsoleLogin",
                "userIdentity": {
                    "type": "Root",
                    "arn": "arn:aws:iam::123456789112:root",
                    "principalId": "123456789112",
                    "accountId": "123456789112"},
                "eventSource": "signin.amazonaws.com",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                "sourceIPAddress": "67.172.93.116"},
            "detail-type": "AWS Console Sign In via CloudTrail",
            "source": "aws.signin",
            "version": "0",
            "time": "2017-09-24T10:35:41Z",
            "id": "b23632a3-4aab-ba5e-3653-789209f5b86e",
            "resources": []},
        None)
