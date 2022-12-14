#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Send_Email import SendEmail
from Create_Email import CreateEmail
from Build_Table import BuildTable
from Event_Parser import EventParser

import logging
import os

# Set up logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Grab variables from environment
# The sender and receiver need to be authorized
# In AWS SES
to_email = os.getenv('TO_EMAIL')
from_email = os.getenv('FROM_EMAIL')


def lambda_handler(event, context):

    # Attempt to locate each of the user properties

    # Grab variables from environment
    #to_email = os.getenv['TO_EMAIL']
    #from_email = os.getenv['FROM_EMAIL']

    parser = EventParser(event)
    parsed_event = parser._parse()

    # Build custom event object
    custom_event = {
        "user_arn": parsed_event['user_arn'],
        "account_id": parsed_event['account_id'],
        "sourceIPAddress": parsed_event['sourceIPAddress'],
        "event_name": parsed_event['event_name'],
        "event_time": parsed_event['event_time'],
        "event_type": parsed_event['event_type']}

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
