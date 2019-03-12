import boto3
import re
import requests
from requests_aws4auth import AWS4Auth
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection

region = 'eu-west-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
host = 'https://vpc-customer360-es-domain-mfwii4yipk4hcr4i2rmdgh2ls4.eu-west-1.es.amazonaws.com'

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

print(es)

index_tmp = 'customer-activities-index-day-'
s3 = boto3.client('s3')
print(s3)

# Lambda execution starts here
def handler(event, context):
    for record in event['Records']:

        # Get the bucket name and key for the new file
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(bucket)
        print(key)

        # Get, read, and split the file into lines
        obj = s3.get_object(Bucket=bucket, Key=key)
        print(obj)
        body = obj['Body'].read()
        print(body)
        lines = body.splitlines()
        print(lines)
        
        # Match the regular expressions to each line and index the JSON
        for line in lines:
            activity = json.dumps(line)
            date = str(activity['activity_date'])
            index = index_tmp + date
            es.index(index=index, doc_type="_doc", body=activity)