import base64
import logging
import json
import re
from logging.config import fileConfig
from botocore.exceptions import ClientError

fileConfig('logging_config.ini')
logger = logging.getLogger()

def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data

def create_group_policies(client, policies): 
    for p in policies:
        add_policy_to_group(client, p['PolicyJsonPath'], p['PolicyName'], p['Group'])

def add_policy_to_group(client, json_path, policy_name, group):
    policy_doc = json.dumps(read_json(json_path), indent=2)
    try:
        logger.info('IAM Roles: Attach policy [{p}] to group [{g}].'.format(p=policy_name, g=group))
        client.put_group_policy(
            GroupName=group,
            PolicyName=policy_name,
            PolicyDocument=policy_doc
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            logger.info('IAM Roles: Policy [{p}] Already Exists. Will Skip this step'.format(p=policy_name))
        else:
            logger.info('Unhandled exception when creating group policy: [{p}]'.format(p=policy_name))
            raise e

def get_db_buckets_arn(username):
    arn = 'arn:aws:s3:::customer360-' + username + '*'
    arn_recursive = arn + '/*'
    return [arn, arn_recursive]

def get_denied_gluedb(username, generic_arn):
    # get all numbers from 0 to 50 as padded strings
    no_list = list(map(lambda x: 'username' + str(x).zfill(2), list(range(1, 35))))
    exclude_list = list(filter(lambda x: x!=username, no_list))
    exclude_arns = list(map(lambda x: generic_arn + x + '*', exclude_list))
    exclude_arns.append(generic_arn + 'default')
    return exclude_arns

def create_user_policies(client, policies, user):
    for p in policies:
        policy_doc = read_json(p['PolicyJsonPath'])
        if p['PolicyName'] == 'Customer360GlueAccessPolicy':
            resources = get_denied_gluedb(user['username'], policy_doc['Statement'][0]['Resource'])
            policy_doc['Statement'][0]['Resource'] = resources
        elif p['PolicyName'] == 'Customer360S3DataLakePolicy':
            resources = get_db_buckets_arn(user['username'])
            policy_doc['Statement'][0]['Resource'] = resources
        add_policy_to_user(client, json.dumps(policy_doc, indent=2), p['PolicyName'], user['username'])    

def add_policy_to_user(client, json_stmt, policy_name, user):
    try:
        logger.info('IAM Roles: Attach policy [{p}] to user [{u}].'.format(p=policy_name, u=user))
        client.put_user_policy(
            UserName=user,
            PolicyName=policy_name,
            PolicyDocument=json_stmt
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            logger.info('IAM Roles: Policy [{p}] Already Exists. Will Skip this step'.format(p=policy_name))
        else:
            logger.info('Unhandled exception when creating user policy: [{p}]'.format(p=policy_name))
            raise e
