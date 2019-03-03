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
        user_aws = client.User(user['username'])
        user_aws.create_login_profile(
            Password=user['password'],
            PasswordResetRequired=False
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
    try:
        group = client.Group(user['group'])
        group.add_user(UserName = user['username'])
        logger.info('User: {username} has been added to the group: {group}'.format(username=user['username'], group=user['group']))
    except ClientError as e:
        group.create()
        logger.info('Group: {group} does not exists. Group will be created'.format(username=user['username'], group=user['group']))
        group.add_user(UserName = user['username'])
        logger.info('User: {username} has been added to the group: {group}'.format(username=user['username'], group=user['group']))