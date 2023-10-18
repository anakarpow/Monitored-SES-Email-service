import json

import boto3

AWS_REGION = "eu-west-1"


client = boto3.client('ses', region_name=AWS_REGION)

response = client.get_send_statistics()

print(json.dumps(response, indent=4, sort_keys=True, default=str))
