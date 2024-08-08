import os
import sys
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError
from monitoring_email_html import format_monitoring_email
from text import monitoring_text

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")

from adresses import receiver_monitoring_email, sender, sender_monitoring_email

ses_client = boto3.client("ses", region_name="eu-west-1")
s3_client = boto3.client('s3')

def monitor_sending(sending_list, success_list, failed_list):
    """
    crosschecks nr of emails succefully sent to SES API against sending_list
    sends reporting email if not equal
    returns status and failed emails 
    """

    send_monitoring_email(success_list, failed_list)

    if len(success_list) < len(sending_list):
        print(f'Not all {len(sending_list)} email have been sent !')
        print("Failed email for following projects")
        for item in failed_list:

            item_key = get_item_key_name(item)
            
            print(f" {item['delivery'][item_key]}")
        status = 0
    else:
        status = 1
        failed_list = []

    # this object is then returned at runtime end &
    # to triggering function
    return {'status': status, 'failed_list': failed_list}

def match_file(file_list, item):
    """
    matches item_key with file_list
    returns file connection inclusive binary data
    attachment key in event no longer needed
    """

    item_key = get_item_key_name(item)

    if (item['email'] == 0):
        return 'MAILNOTFOUND'
    if 'test' in item:
        return 'TEST'
    try:
        file_name = [
            report for report in file_list if item[item_key] in report][0]
    except IndexError:
        print(f"Could not find CR for {item[item_key]}.")
        return 'NOMATCHINGFILE'
    try:
        file = s3_client.get_object(Key=file_name, Bucket=input_bucket)
        return file
    except ClientError as e:
        print(e)
        return 'FILENOTFOUND'

def process_sending_list(event):
    """
    retrieves email list and adds timestamp
    future potential data to b added here
    """
    # retrieve sending data from event and add timestamp
    sending_list = event['adresses']
    timestamp = event['month'].split('/')[:2]
    timestamp = f'{timestamp[1]}/{timestamp[0]}'
    timestamp = datetime.strptime(timestamp, '%m/%Y').date()
    for item in sending_list:
        item['timestamp'] = timestamp
    return sending_list


def list_bucket_files_with_date(s3, bucket, event):
    """
    lists objects in specified bucket according to event month and year
    """
    files = []
    response = s3.list_objects_v2(Bucket=bucket, Prefix=event['month'])

    for content in response.get('Contents', []):
        files.append(content.get('Key'))
    return files


def send_monitoring_email(success_list, failed_list):
    """
    sends reporting email on sending status 
    attaches list of failed emails
    """

    remove_keys = ['project', 'forecast', 'cost_limit',
                   'timestamp', 'project_name', 'email', 'CostCenter']
    # remove info, return report dict
    for failed_email, success_email in zip(failed_list, success_list):
        for key in remove_keys:
            try:
                failed_email.pop(key)
                success_email.pop(key)
            except KeyError:
                pass

    # sendig coordinates
    SENDER = sender_monitoring_email
    RECIPIENT = receiver_monitoring_email
    msg = MIMEMultipart()
    msg["Subject"] = "This is CAST monitoring service: news about SES "
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    # gather email text
    email_text = monitoring_text(failed_list)
    # and attacemnt
    filename = format_monitoring_email(success_list, failed_list)
    with open(filename, 'r') as content_file:
        attachment = content_file.read()

    # attachment
    part = MIMEApplication(attachment)
    part.add_header("Content-Disposition",
                    "attachment",
                    filename=filename.split('/')[2])
    msg.attach(part)

    body = MIMEText(email_text)
    msg.attach(body)

    ses_client.send_raw_email(
        Source=SENDER,
        Destinations=[msg['To']],
        RawMessage={"Data": msg.as_string()}
    )
    print('Monitoring email sent')
    return


def get_item_key_name(item):

    """
        decides the key to be used dependend on the report type
    """

    item_key = 'project_name'
    if 'CostCenter' in item:
        item_key = 'CostCenter'
    
    return item_key