# AWS Event Manager

This program is meant to be ran as a Lambda function in AWS, as it transforms JSON Events from CloudWatch Events, CloudWatch Logs Metric Filters, and other (future) events into friendly HTML emails for end users:

* Pulls identity information and event information from the event and sends as HTML email, easy to read format
* Transforms full JSON event into HTML table for simpler navigation (when reading the full event details)
* Python3.10/Boto3

To use this function, all that is required is to add the *TO_EMAIL* and *FROM_EMAIL* environment variables to the lambda function. The values will be email address of the sender andd receier, as authorized byy AWS SES. 

A diagram of the architecture of this system can be seen below:

![alt text](mailer-diagram.png "AWS EM Serverless Mailer" )

## Email Message

Right now, the email message uses a simple free template, which we import in Python, and template using the jinja2 template library. At the moment, this is simply
a simple black and white template that displays the template properties for the user. This template will likely change, and we aren't set in stone on the colors or columns, etc.

![alt text](email-example.png "Example User Email")

## Support for Various Events

**Important** This function supports thousands of events, due to the fact that most events use a few event message schemas. However, it is outside of our control to enforce consistency on event schemas, and so if event messages deviate from that standard, and if the function has not been updated to account for that structure, the full message details are transformed into an HTML table, instead of the select properties..

Future Improvements

* Add Terraform module for deploying the solution, SES, Lambda function, and related resources. 
* A version of this could, of course, be made using SNS as the delivery mecchanism (w/email subscriber). This would be cheaper, but loses the ability to send HTML formatted emails. 

