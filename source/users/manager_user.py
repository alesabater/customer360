import logging
import json
from logging.config import fileConfig
from botocore.exceptions import ClientError

fileConfig('logging_config.ini')
logger = logging.getLogger()
tags = [{'Key': 'IsWork','Value': 'true'},{'Key': 'WorkType','Value': 'customer360'}]


def iam_create_user(client, user, override=False):
    try:
        client.create_user(
            UserName=user['username'],
            Tags=tags)
        logger.info('User: {username} has been created'.format(username=user['username']))
        print(user['username'])
        #user_aws = client.get_user(UserName=user['username'])
        client.create_login_profile(
            Password=user['password'],
            PasswordResetRequired=False,
            UserName=user['username']
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            if not (override):
                logger.info('User: {username} already exist and override flag is: {override}'.format(username=user['username'], override=override)) 
            else:
                logger.info('User: {username} already exist but override flag is: {override}. User will be re-created. NOT IMPLEMENTED'.format(username=user['username'], override=override))
        else:
            logger.info('Unhandled error. Please check your code.')
            raise e
    client.add_user_to_group(
            GroupName=user['Group'],
            UserName=user['username']
    )

def iam_create_group(client, group):
    try:
        group = client.create_group(
            Path="/",
            GroupName=group
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            logger.info('Group: {g} already exist. Will skip the group creation step'.format(g=group)) 
        else:
            logger.info('Unhandled error when creating group. Please check your code.')
            raise e
    