import json

import boto3
from adress import sending_list

client = boto3.client('lambda')


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
        Payload=json.dumps(sending_list)
    )
    print(resp['Payload'].read())


if __name__ == "__main__":
    lambda_handler(None, None)
