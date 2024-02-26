
import json
import os

import boto3

is_local = os.environ.get("local")

client = boto3.client('lambda')
if is_local:
    print('local version ')
    # event = '../events/base_event.json'
    event = '../events/test.json'

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
        LogType='None',
        Payload=json.dumps(event)
    )
    print(event)
    outcome = resp['Payload'].read()
    print(outcome)
    # if 'Runtime.MarshalError' in str(outcome):
    #     result = 'Something went wrong! please check the CR avaiability in the bucket and control the sending report in your email client'
    # else:
    #     result = outcome
    # print(result)

    # try:
    #     print(resp['Payload'].read())
    # except Exception as e:
    #     print(e)


if __name__ == "__main__":
    lambda_handler(event, None)
