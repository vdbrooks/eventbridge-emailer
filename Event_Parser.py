#from jinja2 import Environment, PackageLoader

# Loads templates from the yourapp.templates folder
#env = Environment(loader=PackageLoader('emailer', 'templates'), autoescape=True)
import logging
#from msilib.schema import Error

# Set up logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EventParser(object):
    def __init__(self, event):
        self.event = event
        self.parsed_event = {}

    def get_event_values(self):
        self.parsed_event['policy_user'] = self.parse_policy_user()
        self.parsed_event['policy_arn'] = self.parse_policy_arn()
        self.parsed_event['user_arn'] = self.parse_user_arn()
        self.parsed_event['account_id'] = self.parse_account_id()
        self.parsed_event['sourceIPAddress'] = self.parse_source_ip()
        self.parsed_event['event_name'] = self.parse_event_name()
        self.parsed_event['event_time'] = self.parse_event_time()
        self.parsed_event['event_type'] = self.parse_event_type()

        return self.parsed_event

    def parse_policy_user(self):
        try:
            policy_user = self.event['detail']['requestParameters']['userName']
        except KeyError as e:
            logging.error("Couldn't find polic user or arn: {0}".format(e))
        return policy_user

    def parse_policy_arn(self):
        try:
            policy_arn = self.event['detail']['requestParameters']['policyArn']
        except KeyError as e:
            logging.error("Couldn't find policy user or arn: {0}".format(e))
        return policy_arn

    def parse_user_arn(self):
        try:
            user_arn = self.event['userIdentity']['arn']
        except KeyError as e:
            try:
                user_arn = self.event['detail']['userIdentity']['arn']
            except KeyError as e:
                user_arn = self.event['userIdentity']['invokedBy']

        return user_arn

    def parse_account_id(self):
        try:
            account_id = self.event['userIdentity']['accountId']
        except KeyError as e:
            try:
                account_id = self.event['detail']['userIdentity']['accountId']
            except KeyError as e:
                account_id = self.event['recipientAccountId']

        return account_id

    def parse_source_ip(self):
        try:
            sourceIPAddress = self.event['sourceIPAddress']
        except KeyError as e:
            sourceIPAddress = self.event['detail']['sourceIPAddress']
            #self.parsed_event['sourceIPAddress'] = sourceIPAddress
        return sourceIPAddress

    def parse_event_name(self):
        try:
            event_name = self.event['eventName']

        except KeyError as e:
            event_name = self.event['detail']['eventName']
            #self.parsed_event['event_name'] = event_name
        return event_name

    def parse_event_time(self):
        try:
            event_time = self.event['eventTime']
        except KeyError as e:
            event_time = self.event['detail']['eventTime']
            #self.parsed_event['event_time'] = event_time
        return event_time

    def parse_event_type(self):
        try:
            event_type = self.event['eventType']
        except KeyError as e:
            event_type = self.event['detail']['eventType']
            #self.parsed_event['event_type'] = event_type
        return event_type
