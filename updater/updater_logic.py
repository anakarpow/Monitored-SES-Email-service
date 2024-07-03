import pandas as pd
from api_utils import query_and_return_dict
import utils
import json
import boto3
import os

def lambda_handler(event, context):
        
    # test data for local
    # file = 'test_data/Output (9).json'
    # with open(file, 'r') as foo:
    #     data = json.load(foo)

    s3 = boto3.client('s3')
    client = boto3.client('lambda')
    
    query_input_bucket = os.environ.get("BUCKET_INPUT_OVERVIEW")
    #'vw-lambda-reporting-manual-input'


    # query API
    data=query_and_return_dict(s3, query_input_bucket)

    # unpack dict, return df with output info
    output_df = utils.extract_contact_and_account_data(data)

    test_json = output_df.to_dict(orient='records')
    with open('test_data/draft_result.json', 'w') as file:
        json.dump(test_json, file)

    # once data workflow is done
    # if output_df is not empty
        # invoke lambda sending payload
    if len(output_df) > 0:
        response = client.invoke(
                FunctionName='CAST-CRS-Sender',
                InvocationType='RequestResponse',
                Payload=test_json,
            )
        print(response['Payload'].read())
    return

if __name__ == "__main__":
    lambda_handler(None, None)