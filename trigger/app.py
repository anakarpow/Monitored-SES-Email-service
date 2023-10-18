import json

import boto3
from adress import sending_list

client = boto3.client('lambda')


def lambda_handler(event, context):

    resp = client.invoke(
        FunctionName='CAST-SES-SendingFunction-xrjocP36snCR',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(sending_list)
    )
    print(resp['Payload'].read())


if __name__ == "__main__":
    lambda_handler(None, None)
