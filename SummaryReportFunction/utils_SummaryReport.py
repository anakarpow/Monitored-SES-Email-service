import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from text_SummaryReport import default_text

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
        item['attachment'] = match_file(file_list, item, 'CostCenter')
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
    sending_report = monitor_sending(sending_list, success_list, failed_list, 'CostCenter')
    return sending_report


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


