import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from text import default_text
from utils import (
    monitor_sending,
    match_file,
    # send_email_with_attachment
)

from adresses import sender

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")


ses_client = boto3.client("ses", region_name="eu-west-1")
s3_client = boto3.client('s3')


def sending_loop(sending_list, file_list, email_template):
    """
    iterates sending_list, matching file by project name
    sends email
    adds metadata on sending process 
    calls monitoring function
    """
    # start reporting lists
    success_list = []
    failed_list = []
    for item in sending_list:
        # get respective file
        item['attachment'] = match_file(file_list, item)
        # send email
        resp = send_email_with_attachment(
            item, email_template)
        # attaching meta info to resp
        resp['delivery'] = {"project_name": item['project_name'],
                            "email_adress": item['email']}
        if 'MessageId' in resp:
            success_list.append(resp)
        else:
            failed_list.append(resp)

    # checking nr of sent emails against adress list
    sending_report = monitor_sending(sending_list, success_list, failed_list)
    return sending_report


def send_email_with_attachment(item, email_template):
    """
    compose and send email
    """
    if (item['attachment'] == 'FILE-NOT-FOUND') or (item['attachment'] == 'GET-ERROR') or (item['attachment'] == 'MAIL-NOT-FOUND'):
        item.pop('timestamp')
        return item

    item['timestamp'] = item['timestamp'].strftime('%B %Y')
    # sendig coordinates
    SENDER = sender
    RECIPIENT = item['email']
    msg = MIMEMultipart()
    msg["Subject"] = f"Monthly Report for {item['project_name']} {item['timestamp']} "
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    email_text = default_text(email_template, variables=item)
    body = MIMEText(email_text, "html")
    msg.attach(body)

    try:
        part = MIMEApplication(item['attachment']['Body'].read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=f"{item['project_name']}.html")
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


def get_email_template(s3, input_bucket):
    """
    retrieves email_template from bucket
    """
    files = []
    response = s3.list_objects_v2(
        Bucket=input_bucket, Prefix='email_templates')
    for content in response.get("Contents", []):
        if not content.get("Key").endswith("/"):
            files.append(content.get("Key"))

    if len(files) < 1:
        print('No email template was found in the bucket ')
        exit()

    query = s3.get_object(Bucket=input_bucket, Key=files[0])
    query = query["Body"].read().decode("utf-8")
    print("standard email_template loaded from bucket")
    return query


