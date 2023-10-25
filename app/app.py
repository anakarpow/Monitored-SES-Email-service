
import json
import os

import boto3
from utils import list_bucket_files_with_date, process_sending_list, sending_loop

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")

# receives trigger from CR function with : month of interest to retrieve CR from S3, list of adresses
if is_local:
    event = 'events/test0_aws.json'
    with open(event, 'r') as file:
        event = json.load(file)

s3_client = boto3.client('s3')


def lambda_handler(event, context):

    # get all CR for selected month
    file_list = list_bucket_files_with_date(
        s3_client, bucket=input_bucket, event=event)

    # work on sending list
    sending_list = process_sending_list(event)

    # iterate sending list and send emails
    sending_report = sending_loop(sending_list, file_list)

    return sending_report


if __name__ == "__main__":
    lambda_handler(event, None)
