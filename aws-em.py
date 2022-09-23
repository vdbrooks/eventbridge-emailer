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
    parsed_event = parser.get_event_values()

    print(parsed_event)
    # Build custom event object
    print("Here is the value of the parsed event \n")
    print(parsed_event)
    custom_event = {
        "user_arn": parsed_event['user_arn'],
        "account_id": parsed_event['account_id'],
        "sourceIPAddress": parsed_event['sourceIPAddress'],
        "event_name": parsed_event['event_name'],
        "event_time": parsed_event['event_time'],
        "event_type": parsed_event['event_type'],
        "policy_arn": parsed_event['policy_arn'],
        "policy_user": parsed_event['policy_user']}

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
            "version": "0",
            "id": "2be0546a-38fe-2b9c-2be9-56268b6bcb0b",
            "detail-type": "AWS API Call via CloudTrail",
            "source": "aws.iam",
            "account": "123456789112",
            "time": "2022-09-17T03:30:05Z",
            "region": "us-east-1",
            "resources": [],
            "detail": {
                "eventVersion": "1.08",
                "userIdentity": {
                    "type": "Root",
                    "principalId": "123456789112",
                    "arn": "arn:aws:iam::123456789112:root",
                    "accountId": "123456789112",
                    "accessKeyId": "ASIA4PVLGHWZMDDHBFGET",
                    "sessionContext": {
                        "sessionIssuer": {},
                        "webIdFederationData": {},
                        "attributes": {
                            "creationDate": "2022-09-17T02:21:37Z",
                            "mfaAuthenticated": "true"}}},
                "eventTime": "2022-09-17T03:30:05Z",
                "eventSource": "iam.amazonaws.com",
                "eventName": "AttachUserPolicy",
                "awsRegion": "us-east-1",
                "sourceIPAddress": "AWS Internal",
                "userAgent": "AWS Internal",
                        "requestParameters": {
                            "userName": "new_user",
                            "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess"},
                "responseElements": "null",
                "requestID": "4a949ee0-0511-41d3-ac1f-eaa39d6adee7",
                "eventID": "0a9b1e24-8f9a-4fd6-90d9-ac2efa8ee53c",
                "readOnly": "false",
                            "eventType": "AwsApiCall",
                            "managementEvent": "true",
                            "recipientAccountId": "1234567899112",
                            "eventCategory": "Management",
                            "sessionCredentialFromConsole": "true"}},
        None)
