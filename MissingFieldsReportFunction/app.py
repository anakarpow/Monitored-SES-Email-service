import json
import os
from random import sample

import boto3

from utils_MissingFieldsReport import (
    sending_loop_missing_fields
)

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")

# # receives trigger from CR function with : month of interest to retrieve CR from S3, list of adresses


s3_client = boto3.client('s3')


def lambda_handler(event, context):
    if is_local:
        print('local event version ')
        event = '../events/missing_fields_test.json'

        with open(event, 'r') as file:
            event = json.load(file)

    # function to send the email with missing values

    sending_list = event

    # list of project that have to be sent to CO
    projects_co = []
    for project in event:
        if 'summaryreportcontact' in project['missing_fields']:
            projects_co.append(project['project_name'])

    # send the emails
    # return projects_co
    sending_report = sending_loop_missing_fields(sending_list, projects_co)

    print('Finished')
    return sending_report


if __name__ == "__main__":
    lambda_handler(None, None)
