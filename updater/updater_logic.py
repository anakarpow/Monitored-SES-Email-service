import pandas as pd
from api_utils import query_and_return_dict
import utils
import json
import boto3
import os
is_local = os.environ.get("local")


def lambda_handler(event, context):

    if is_local:
        input_json = 'test_data/Output (12).json'
        with open(input_json, 'r') as file:
            input_data = json.loads(file)
            print(input_data)

    s3 = boto3.client('s3', region_name='eu-west-1')
    client = boto3.client('lambda')

    query_input_bucket = os.environ.get("BUCKET_INPUT_OVERVIEW")

    # query API
    data = query_and_return_dict(s3, query_input_bucket)

    # unpack dict, return df with output info
    output_df = utils.extract_contact_and_account_data(data)

    test_json = output_df.to_dict(orient='records')

    if any(len(i) for i in output_df['missing_fields']) > 0:
        response = client.invoke(
            FunctionName='CAST-CRS-Sender',
            InvocationType='RequestResponse',
            Payload=json.dumps(test_json),
        )
    return


if __name__ == "__main__":
    lambda_handler(None, None)
