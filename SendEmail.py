import boto3


class SendEmail(object):  
    def __init__(self, to, subject, html):
        self.to = to
        self.subject = subject
        self.html = html
        self._text = None


    def send(self, from_addr=None):
        ses = boto3.client('ses',region_name='us-east-1')
        self.from_addr = from_addr

        #Message dictionary
        self. message = {"Body":{"Html":{"Charset":"UTF-8","Data":""},"Text":{"Charset":"UTF-8","Data":"Failed to redner HTML"}},"Subject":{"Charset":"UTF-8","Data":"Test email"}}
        self.message['Body']['Html']['Data'] = self.html
        self.message['Subject']['Data'] = self.subject

        #Destination dictionary
        destination = {"ToAddresses":["recipient1@example.com"]}
        destination['ToAddresses'] = [self.to]
        response = ses.send_email(Source=self.from_addr,Destination=destination,Message=self.message)

