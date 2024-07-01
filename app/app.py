
import json
import os
from random import sample

import boto3
from utils import (
    check_if_test,
    get_email_template,
    list_bucket_files_with_date,
    process_sending_list,
    sending_loop,
)

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")

# receives trigger from CR function with : month of interest to retrieve CR from S3, list of adresses
if is_local:
    print('local event version ')
    # event = '../events/base_event.json'
    event = '../events/test.json'
    # # event = '../events/full_test_event.json'
    # event = '../events/roll_out_Dec.json'

    with open(event, 'r') as file:
        event = json.load(file)

s3_client = boto3.client('s3')


def lambda_handler(event, context):

    # read event and go to specific workflow
    if 'missing_fields' in event:
        # customerDB event
        sample = {"adresses": [
            {"project_name": "name",
             "missing_fields": ['a', 'b', 'c'],
             "email_adresses": ['a', 'b', 'c']}
        ]}
        pass
    # get email template => rewrite func to have prefix as parameter. to use same func for both use cases
    # write new sending loop according to requirements
    # smth like if clearing office in list
        # send to CO
    # else
        # send to tenant
    # make sure to integrate monitor_sending function
    # parameters = sending_list, success_list, failed_list
    # return sending_report like other workflow
    else:
        # if test event add marker to event
        # one email sent to specified adress, without attachement
        event = check_if_test(event)

        # look in bucket for emailtext archive
        # add logic to select the right one
        email_template = get_email_template(s3_client, input_bucket)

        # get all CR for selected month > returns existing CR in S3
        file_list = list_bucket_files_with_date(
            s3_client, bucket=input_bucket, event=event)

        # work on sending list, adding metadata
        sending_list = process_sending_list(event)

        # iterate sending list and send emails, activates monitoring process
        sending_report = sending_loop(sending_list, file_list, email_template)

        print('Finished')
        return sending_report


if __name__ == "__main__":
    lambda_handler(event, None)
