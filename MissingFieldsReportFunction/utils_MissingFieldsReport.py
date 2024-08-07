from adresses import receiver_monitoring_email, sender, sender_monitoring_email
import os
import sys
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError
from monitoring_email_html import format_monitoring_email
from text import default_text, monitoring_text, missing_fields_text, missing_fields_co_text

from utils import (
    monitor_sending,
)

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")


ses_client = boto3.client("ses", region_name="eu-west-1")
s3_client = boto3.client('s3')



def sending_loop_missing_fields(sending_list, projects_co):
    """
    iterates sending_list, matching CR by project name
    sends email
    adds metadata on sending process 
    calls monitoring function
    """
    # start reporting lists
    success_list = []
    failed_list = []
    for item in sending_list:

        for recipient in item['email_adresses']:
            # send email
            resp = send_email_with_missing_fields(
                recipient, item)
        # track the emails that were send (without the CO)
            if resp != 'co':
                resp['delivery'] = {"project_name": item['project_name'],
                                    "email_adress": recipient}
                if 'MessageId' in resp:
                    success_list.append(resp)
                else:
                    failed_list.append(resp)
    # send the emails to CO if there is 'summaryreportcontact' in the missing fields
    if len(projects_co) > 0:
        send_email_to_co(projects_co)

    # if test, dont send montoring email
    if 'test' in item:
        print('Test email sent without monitoring email')
        return {'status': 'test email sent'}

    # checking nr of sent emails against adress list
    sending_report = monitor_sending(sending_list, success_list, failed_list)
    return sending_report


def send_email_with_missing_fields(recipient, item):
    """
    supports attachments but no fine tuning in multiple recipients
    accoridng to testing : all adresses are set as Bcc
    """
    # sendig coordinates
    SENDER = sender

    # send all the missing fields except summaryreportcontact
    if len([field for field in item['missing_fields'] if field != 'summaryreportcontact']) > 0:
        RECIPIENT = recipient
        msg = MIMEMultipart()
        msg["Subject"] = f"DPP Missing Data {item['project_name']} "
        msg["From"] = SENDER
        msg["To"] = RECIPIENT

        email_text = missing_fields_text(variables=item)
        body = MIMEText(email_text, "html")
        msg.attach(body)

        # Convert message to string and send
        try:
            response = ses_client.send_raw_email(
                Source=SENDER,
                Destinations=[msg['To']],
                RawMessage={"Data": msg.as_string()}
            )
            print("Email sent!")
            return response

        # Display an error if something goes wrong.
        except Exception as e:
            print(e)
            return {}
    else:
        return 'co'


def send_email_to_co(projects_co):
    """
    supports attachments but no fine tuning in multiple recipients
    accoridng to testing : all adresses are set as Bcc
    """
    # sendig coordinates
    SENDER = sender
    RECIPIENT = receiver_monitoring_email

    msg = MIMEMultipart()
    msg["Subject"] = f"DPP Missing Data For Clearing Office"
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    # send the email to CO with the names of the projects
    email_text = missing_fields_co_text(projects_co)
    body = MIMEText(email_text, "html")
    msg.attach(body)

    # Convert message to string and send
    try:
        response = ses_client.send_raw_email(
            Source=SENDER,
            Destinations=[msg['To']],
            RawMessage={"Data": msg.as_string()}
        )
        print("Email to CO sent!")
        return response

    # Display an error if something goes wrong.
    except Exception as e:
        print(e)
        return {}
