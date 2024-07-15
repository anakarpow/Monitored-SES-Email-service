import pandas as pd
from api_utils import query_and_return_dict
import utils
import json
import boto3
import os
from datetime import datetime
import io
is_local = os.environ.get("local")

s3 = boto3.client('s3', region_name='eu-west-1')
client = boto3.client('lambda', region_name='eu-west-1')


def lambda_handler(event, context):

    # read sample data in local version
    if is_local:
        input_json = 'test_data/Output.json'
        with open(input_json, 'r') as file:
            data = json.load(file)
    # query API in cloud version
    else:
        query_input_bucket = os.environ.get("BUCKET_INPUT_OVERVIEW")
        # query API
        data = query_and_return_dict(s3, query_input_bucket)

    # unpack dict, return df with output info
    output_df = utils.extract_contact_and_account_data(data)
    sending_json = output_df.to_dict(orient='records')

    # save to local data
    if is_local:
        with open('test_data/draft_result.json', 'w') as file:
            json.dump(sending_json, file)

        output_df[['project_name', 'missing_fields']].to_csv(
            'test_data/draft_result.csv', index=False)
        return

    else:

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                output_df[['project_name', 'missing_fields']].to_excel(writer)
                data = output.getvalue()
                s3.upload_fileobj(io.BytesIO(data), 'cast-output-dev',
                                  'customer_data_updates/missing_fields' + str(datetime.now()) + '.xlsx')

        # stop here to avoid sending emails
        exit()
        # invoke SES Lambda
        if any(len(i) for i in output_df['missing_fields']) > 0:
            response = client.invoke(
                FunctionName='CAST-CRS-Sender',
                InvocationType='RequestResponse',
                Payload=json.dumps(test_json),
            )
        return


if __name__ == "__main__":
    lambda_handler(None, None)
