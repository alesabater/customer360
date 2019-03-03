import base64
import logging
import json
import re
from logging.config import fileConfig
from botocore.exceptions import ClientError

fileConfig('logging_config.ini')
logger = logging.getLogger()

def get_regex_or_none(pattern, s):
    r = re.search(pattern, s)
    if r is not None:
        return r.group(0)
    else:
        return None

def delete_participant_bucket(client, bucket):
    try: 
        logger.info('Deleting S3 Bucket: [{bucket}]'.format(bucket=bucket))
        response = client.delete_bucket(Bucket=bucket)
        return response
    except ClientError as e:
        logger.info('Unhandled exception when deleting S3 Bucket: [{bucket}]'.format(bucket=bucket))
        raise e


def delete_participant_buckets(client, user): 
    p = "^customer360-{user}-.*".format(user=user)
    response = client.list_buckets()
    buckets = list(map(lambda x: x['Name'], response['Buckets']))
    buckets_delete = list(filter(None, list(map(lambda x: get_regex_or_none(p, x), buckets))))
    buckets_str = ", ".join(buckets_delete)
    print(buckets_delete)
    logger.info('Deleting S3 Buckets: [{buckets}]'.format(buckets=buckets_str))
    delete_response = list(map(lambda x: delete_participant_bucket(client, x), buckets_delete))
    logger.info('Buckets deleted successfully')
    return delete_response

def create_participant_bucket(client, bucket, region='eu-west-1'):
    try: 
        logger.info('Creating S3 Bucket: [{bucket}]'.format(bucket=bucket))
        response = client.create_bucket(ACL = 'private', Bucket = bucket, CreateBucketConfiguration = {'LocationConstraint':region})
        response['bucket_secret'] = {'{bucket}: SUCCEEDED'.format(bucket=bucket)}
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            logger.info('S3 Bucket: [{bucket}] Already Exists. Will Skip this step'.format(bucket=bucket))
            e.response['bucket_secret'] = {'{bucket}: EXISTS'.format(bucket=bucket)}
            return e.response
        else:
            logger.info('Unhandled exception when creating S3 Bucket: [{bucket}]'.format(bucket=bucket))
            raise e

def create_participant_buckets(client, bucket_list, region='eu-west-1'):
    buckets_str = ", ".join(bucket_list)
    logger.info('List of S3 Buckets: [{buckets}]'.format(buckets=buckets_str))
    responses = list(map(lambda x: create_participant_bucket(client, x, region), bucket_list))
    logger.info('Buckets created successfully')
    return responses



