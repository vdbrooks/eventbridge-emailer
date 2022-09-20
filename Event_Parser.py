#from jinja2 import Environment, PackageLoader

# Loads templates from the yourapp.templates folder
#env = Environment(loader=PackageLoader('emailer', 'templates'), autoescape=True)


class EventParser(object):
    def __init__(self, event):
        self.event = event
        self.parsed_event = {}

    def _parse(self):
        #parsed_event = {}
        try:
            user_arn = self.event['userIdentity']['arn']
            self.parsed_event['user_arn'] = user_arn
        except KeyError as e:
            try:
                user_arn = self.event['detail']['userIdentity']['arn']
                self.parsed_event['user_arn'] = user_arn
            except KeyError as e:
                #logging.error('Trying last attempt to get userIdentity: {0} '.format(e))
                user_arn = self.event['userIdentity']['invokedBy']
                self.parsed_event['user_arn'] = user_arn

        try:
            account_id = self.event['userIdentity']['accountId']
            self.parsed_event['account_id'] = account_id
        except KeyError as e:
            try:
                account_id = self.event['detail']['userIdentity']['accountId']
                self.parsed_event['account_id'] = account_id
            except KeyError as e:
                account_id = self.event['recipientAccountId']
                self.parsed_event['account_id'] = account_id

        try:
            sourceIPAddress = self.event['sourceIPAddress']
            self.parsed_event['sourceIPAddress'] = sourceIPAddress
        except KeyError as e:
            sourceIPAddress = self.event['detail']['sourceIPAddress']
            self.parsed_event['sourceIPAddress'] = sourceIPAddress

    # Attempt to locate each of the event  properties

        try:
            event_name = self.event['eventName']
            self.parsed_event['event_name'] = event_name
        except KeyError as e:
            event_name = self.event['detail']['eventName']
            self.parsed_event['event_name'] = event_name

        try:
            event_time = self.event['eventTime']
            self.parsed_event['event_time'] = event_time
        except KeyError as e:
            event_time = self.event['detail']['eventTime']
            self.parsed_event['event_time'] = event_time

        try:
            event_type = self.event['eventType']
            self.parsed_event['event_type'] = event_type
        except KeyError as e:
            event_type = self.event['detail']['eventType']
            self.parsed_event['event_type'] = event_type
        
        return self.parsed_event
