import json
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from adresses import receiver_monitoring_email, sender, sender_monitoring_email
from text import default_text, monitoring_text

is_local = os.environ.get("local")

ses_client = boto3.client("ses", region_name="eu-west-1")
s3_client = boto3.client('s3')
bucket = 'vw-lambda-reporting-output'


def match_file(file_list, item):
    """
    matches project_name with file_list
    returns file connection inclusive binary data
    attachment key in event no longer needed
    """
    file_name = [x for x in file_list if item['project_name'] in x][0]
    if len(file_name) == 0:
        print('file not found ERROR')
        exit()
    file = s3_client.get_object(Key=file_name, Bucket=bucket)
    return file


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

    # sendig coordinates
    SENDER = sender
    RECIPIENT = item['email']
    msg = MIMEMultipart()
    msg["Subject"] = f"DPP Cost Report {item['project_name']} {item['timestamp']} "
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    # text variables
    # in the future import text from S3
    # Set message body, adding variables.
    email_text = default_text(variables=item)

    body = MIMEText(email_text, "html")
    msg.attach(body)

    try:
        # In same directory as script
        # with open(item['attachment'], "rb") as attachment_data:
        # with item['attachment']['Body'].read() as attachment_data:
        part = MIMEApplication(item['attachment']['Body'].read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=item['project_name'])
        msg.attach(part)

        # Convert message to string and send
        response = ses_client.send_raw_email(
            Source=SENDER,
            Destinations=[msg['To']],
            RawMessage={"Data": msg.as_string()}
        )
        print("Email sent!")
        return response

    # Display an error if something goes wrong.
    except (FileNotFoundError)as e:
        print(e)
        return {}


def send_monitoring_email(failed_list):

    # sendig coordinates
    SENDER = sender_monitoring_email
    RECIPIENT = receiver_monitoring_email

    msg = MIMEMultipart()
    msg["Subject"] = "This is CAST monitoring service: news about SES "
    msg["From"] = SENDER
    msg["To"] = RECIPIENT

    email_text = monitoring_text(failed_list)
    body = MIMEText(email_text, "html")
    msg.attach(body)

    ses_client.send_raw_email(
        Source=SENDER,
        Destinations=[msg['To']],
        RawMessage={"Data": msg.as_string()}
    )


if __name__ == "__main__":
    filename = '../output/2023-06-DPP-AUDI AG-AUDINECKARSULMDATALAKE.html'
    with open('../test_data/main_dict_5_2022.json', 'r') as file:
        data = json.load(file)
        for project, values in data.items():
            send_email_with_attachment(data[project], filename)
            exit()
