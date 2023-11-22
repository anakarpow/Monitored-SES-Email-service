
import json
import os

import boto3

is_local = os.environ.get("local")

client = boto3.client('lambda')
if is_local:
    print('local version ')
    event = '../events/base_event.json'
    with open(event, 'r') as file:
        event = json.load(file)


def lambda_handler(event, context):

    # paginator handles repsnses longer than 50 obj
    func_paginator = client.get_paginator('list_functions')
    for func_page in func_paginator.paginate():
        for func in func_page['Functions']:
            if 'Sending' in func['FunctionName']:
                sending_func = func['FunctionName']
                print(sending_func)

    resp = client.invoke(
        FunctionName=sending_func,
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(event)
    )
    print(resp['Payload'].read())


if __name__ == "__main__":
    lambda_handler(None, None)
