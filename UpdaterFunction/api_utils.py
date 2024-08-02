
import os
import boto3
from requests_aws4auth import AWS4Auth
import json
import requests


def query_and_return_dict(s3, query_input_bucket):
    # get credentials to assume extra role
    credentials = get_credentials_role()
    # use credentials to access a appsync client
    client = make_client(credentials)
    # retrieve query from bucket
    query = get_query(s3, query_input_bucket)
    # use Outbound Proxy to connect to external API
    proxies = get_proxy_url()
    # launch query and save json to tmp
    customer_data = test_get(client, query, proxies)
    return customer_data


def get_credentials_role():
    """
    get credentials to assume DB API role
    """
    api_role = os.environ.get('API_ROLE')
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=api_role, RoleSessionName="cast-api-session")

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    print(" Credentials retrived")
    credentials = {'access': ACCESS_KEY,
                   'key': SECRET_KEY, 'token': SESSION_TOKEN}

    return credentials


def make_client(credentials):
    """
    creates Appsync client with custom credentials
    """
    try:
        auth = AWS4Auth(
            credentials["access"],
            credentials["key"],
            "eu-west-1",
            "appsync",
            session_token=credentials["token"],
        )
    except Exception as e:
        print(e)

    # transport = RequestsHTTPTransport(url=url, headers=headers, auth=auth)
    # client = Client(transport=transport, fetch_schema_from_transport=False)

    print("Appsync client created: ready for API query")

    return auth


def get_query(s3, input_bucket):
    """
    retrieves query text from bucket
    """
    files = []
    response = s3.list_objects_v2(Bucket=input_bucket)
    for content in response.get('Contents', []):
        if not content.get('Key').endswith('/'):
            if 'query' in content.get('Key'):
                files.append(content.get('Key'))

    print(files)
    query = s3.get_object(Bucket=input_bucket, Key=files[0])

    query = query['Body'].read().decode('utf-8')
    return query


def get_proxy_url():

    ssm_client = boto3.client('ssm')
    secretmanager_client = boto3.client('secretsmanager')

    # retrieve Arn of the secret with credentials form Parameter Store
    secret = ssm_client.get_parameter(
        Name='/proxy/paas/secret/arn/' + os.environ.get('ProxyId'), WithDecryption=True)
    secret_arn = secret['Parameter']['Value']

    # retrieve secret with credentials
    proxy_credentials_secret = secretmanager_client.get_secret_value(
        SecretId=secret_arn
    )

    # convert convert to json
    proxy_credentials = json.loads(proxy_credentials_secret['SecretString'])

    # create proxy url
    http_proxy = 'https://' + proxy_credentials['username'] + ':' + \
        proxy_credentials['password'] + '@' + 'proxy.saas.vwapps.cloud:8443'
    proxies = {
        'https': http_proxy
    }

    return proxies


def test_get(client, query, proxies):
    """
    queries API using retrieved query text
    """
    url = (
        "https://z2jlkzwg3vgjrk43mykl7zo424.appsync-api.eu-west-1.amazonaws.com/graphql")

    resp = requests.post(url, auth=client, json={
        "query": query}, proxies=proxies)
    print("API response obtained")

    return resp.json()
