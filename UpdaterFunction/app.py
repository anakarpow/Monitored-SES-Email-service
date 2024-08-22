import os
import boto3
import json
from utils import extract_contact_and_account_data, save_missing_fields
from api_utils import query_and_return_dict


is_local = os.environ.get("local")

s3 = boto3.client('s3', region_name='eu-west-1')
client = boto3.client('lambda', region_name='eu-west-1')


def lambda_handler(event, context):

    # read sample data in local version
    if is_local:
        input_json = '../test_data/Output.json'
        with open(input_json, 'r') as file:
            data = json.load(file)
    # query API in cloud version
    else:
        query_input_bucket = os.environ.get("BUCKET_INPUT_OVERVIEW")
        # query API
        data = query_and_return_dict(s3, query_input_bucket)

    # unpack dict, return df with output info
    output_df = extract_contact_and_account_data(data)
    sending_json = output_df.to_dict(orient='records')

    # save to local data

    save_missing_fields(is_local, sending_json, output_df, s3)

    if event['send_email'] == True:

        # invoke SES Lambda
        if is_local:
            print('running local, not sending emails')
            return
        else:
            if any(len(i) for i in output_df['missing_fields']) > 0:
                response = client.invoke(
                    FunctionName='CAST-MFR-Sender',
                    InvocationType='RequestResponse',
                    Payload=json.dumps(sending_json),
                )
            return 


if __name__ == "__main__":
    lambda_handler({"send_email": False}, None)
