import os
import sys
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError
from monitoring_email_html import format_monitoring_email
from text import default_text, monitoring_text


is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")

# if is_local:
#     sys.path.insert(1, '../shared/python')

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
            # print('from monitoring', item)
            print(f" {item['delivery']['CostCenter']}")
        status = 0
    else:
        status = 1
        failed_list = []


    # this object is then returned at runtime end &
    # to triggering function
    return {'status': status, 'failed_list': failed_list}


def sending_loop_summary(sending_list, file_list):
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
        # get respective CR
        item['attachment'] = match_file(file_list, item)
        # send email
        resp = send_email_with_attachment(
            item)
        # attaching meta info to resp
        resp['delivery'] = {"CostCenter": item['CostCenter']}

        if 'MessageId' in resp:
            success_list.append(resp)
        else:
            failed_list.append(resp)

    # if test, dont send montoring email
    if 'test' in item:
        print('Test email sent without monitoring email')
        return {'status': 'test email sent'}
    # checking nr of sent emails against adress list
    sending_report = monitor_sending(sending_list, success_list, failed_list)
    return sending_report


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


def match_file(file_list, item):
    """
    matches project_name with file_list
    returns file connection inclusive binary data
    attachment key in event no longer needed
    """

    if (item['email'] == 0):
        return 'MAILNOTFOUND'
    if 'test' in item:
        return 'TEST'
    try:
        file_name = [
            report for report in file_list if item['CostCenter'] in report][0]
    except IndexError:
        print(f"Could not find CR for {item['CostCenter']}.")
        return 'NOMATCHINGFILE'
    try:
        file = s3_client.get_object(Key=file_name, Bucket=input_bucket)
        return file
    except ClientError as e:
        print(e)
        return 'FILENOTFOUND'


def list_bucket_files_with_date(s3, bucket, event):
    """
    lists objects in specified bucket according to event month and year
    """
    files = []
    response = s3.list_objects_v2(Bucket=bucket, Prefix=event['month'])

    for content in response.get('Contents', []):
        files.append(content.get('Key'))
    return files


def send_email_with_attachment(item):
    """
    supports attachments but no fine tuning in multiple recipients
    accoridng to testing : all adresses are set as Bcc
    """
    if (item['attachment'] == 'FILENOTFOUND') or (item['attachment'] == 'NOMATCHINGFILE') or (item['attachment'] == 'MAILNOTFOUND'):
        item.pop('timestamp')
        return item

    item['timestamp'] = item['timestamp'].strftime('%B %Y')
    # sendig coordinates
    SENDER = sender
    RECIPIENT = item['email']
    msg = MIMEMultipart()
    msg["Subject"] = f"DPP Summary Report {item['CostCenter']} {item['timestamp']} "
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    email_text = default_text(variables=item)
    body = MIMEText(email_text, "html")
    msg.attach(body)

    if item['attachment'] == 'TEST':
        pass
    else:
        try:
            part = MIMEApplication(item['attachment']['Body'].read())
            part.add_header("Content-Disposition",
                            "attachment",
                            filename=f"{item['CostCenter']}.html")
            msg.attach(part)
        except (FileNotFoundError)as e:
            print(e)

    # Convert message to string and send
    try:
        response = ses_client.send_raw_email(
            Source=SENDER,
            Destinations=[msg['To']],
            RawMessage={"Data": msg.as_string()}
        )
        print("Email sent!")
        item.pop('timestamp')
        return response

    # Display an error if something goes wrong.
    except Exception as e:
        print(e)
        return {}


def send_monitoring_email(success_list, failed_list):
    """
    sends reporting email on sending status 
    attaches list of failed emails
    """

    remove_keys = ['project', 'timestamp', 'CostCenter', 'email']
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

