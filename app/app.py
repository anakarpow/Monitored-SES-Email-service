
import json
import os

import boto3
from utils import (
    list_bucket_files_with_date,
    match_file,
    send_email_with_attachment,
    send_monitoring_email,
)

# receives trigger from CR function with : month of interest to retrieve CR from S3, list of adresses
is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")



if is_local:
    event = 'events/test0_aws.json'
    with open(event, 'r') as file:
        event = json.load(file)

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # start reporting lists
    success = []
    failed = []

    # get all CR for selected month
    file_list = list_bucket_files_with_date(
        s3_client, bucket=input_bucket, event=event)

    # retrieve sending data from event
    sending_list = event['adresses']

    # iterate sending list and send emails
    for item in sending_list:
        # get respective CR
        item['attachment'] = match_file(file_list, item)
        # send email
        resp = send_email_with_attachment(
            item)
        # attaching meta info to resp > pack into function TODO
        resp['delivery'] = {"project_name": item['project_name'],
                            "email_adress": item['email']}
        if 'MessageId' in resp:
            success.append(resp)
        else:
            failed.append(resp)

    # checking nr of sent emails against adress list > TODO pack into function
    if len(success) < len(sending_list):
        print(f'Not all {len(sending_list)} email have been sent !')
        print(failed)
        send_monitoring_email(failed)
        status = 0
    else:
        status = 1
        failed = []

    return {'status': status, 'failed': failed}


if __name__ == "__main__":
    lambda_handler(event, None)
