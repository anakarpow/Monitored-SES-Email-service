
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
    sending_loop_misfields,
)

is_local = os.environ.get("local")
input_bucket = os.environ.get("BUCKET_INPUT")
input_bucket_overview = os.environ.get("BUCKET_INPUT_OVERVIEW")

# # receives trigger from CR function with : month of interest to retrieve CR from S3, list of adresses
# if is_local:
#     print('local event version ')
#     # event = '../events/base_event.json'
#     event = '../events/test.json'
#     # # event = '../events/full_test_event.json'
#     # event = '../events/roll_out_Dec.json'

#     with open(event, 'r') as file:
#         event = json.load(file)

s3_client = boto3.client('s3')

event = [
    {
        "email_adresses": [
            "cast.ses.1@efs.at",
            "cast.ses.2@efs.at"
        ],
        "project_name": "TestABC",
        "missing_fields": [
            "wanumber"
        ]
    },
    {
        "email_adresses": [
            "cast.ses.1@efs.at",
            "ClearingOffice"
        ],
        "project_name": "Ice-Cream Detection",
        "missing_fields": [
            "wanumber"
        ]
    },
    {
        "email_adresses": [
            "cast.ses.2@efs.at"
        ],
        "project_name": "Soda-Zitrone",
        "missing_fields": [
            "businessserviceid",
            "billingmethod",
            "dppcentral"        ]
    },
    {
        "email_adresses": [
            "ClearingOffice"
        ],
        "project_name": "For CO Only",
        "missing_fields": [
            "billingmethod"
        ]
    }

]
def lambda_handler(event, context):
    # sending_list = []
    # missing_fields = []
    # read event and go to specific workflow
    
    #if 'missing_fields' in event:
    print(event)
    if len(event) > 0:
        # customerDB event
        sample = {"adresses": [
            {"project_name": "name",
             "missing_fields": ['a', 'b', 'c'],
             "email_adresses": ['a', 'b', 'c']}
        ]}
        #pass
        # for pr in event:
        #     sending_list.append(pr['email_adresses'][0])
        #     missing_fields.append(pr['missing_fields'])

            # send email
    
        # for i in range(len(sending_list)):
            # send to sending_ist[i] 
            # send what: missing_fields[i]

        # get_email_template 
        # => rewrite func get_email_template to have prefix as parameter. to use same func for both use cases 
        # (either updater or cost-reporting) - bucket is always the same -> either 2 different folders or one folder and filter for files 

    # write new sending_loop() according to requirements (ganz neue funktion)
        # for each item in list send the list of missing fileds 
        sending_list = event
        sending_report = sending_loop_misfields(sending_list)

    # smth like if clearing office in list
        # send to CO
    # else
        # send to tenant

    # !!!make sure to integrate monitor_sending function (use as it is -- check if it is so)
    # parameters = sending_list, success_list, failed_list
    
    # return sending_report like other workflow from sending_loop func - rewrite this function

    # no attachments, only text from file from s3 bucket + list of missing fields

    # send_email_with_attachment some parts can be taken forthis part
        print('Finished')
        return sending_report

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
