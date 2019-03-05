import json
import boto3
import argparse
import sys
import logging
import random
import string
import manager_secrets as SecretsMng
import manager_user as UserMng
import manager_s3 as S3Mng
import manager_glue as GlueMng
#from manager_secrets import create_secret
#from manager_user import iam_create_user
from logging.config import fileConfig
from botocore.exceptions import ClientError

fileConfig('logging_config.ini')
logger = logging.getLogger()
tags = [{'Key': 'IsWork','Value': 'true'},{'Key': 'WorkType','Value': 'customer360'}]

def read_users(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_resource_list(user, string_format, staging_areas):
    return list(map(lambda x: string_format.format(username=user, area=x), staging_areas))

def create_user_dict(user, user_meta):
    user_dict = {}
    user_dict['username'] = user
    user_dict['group'] = user_meta['group']
    user_dict['DataStagingAreas'] = user_meta['DataStagingAreas']
    if user_meta['createS3Buckets'] == True:
        user_dict['S3Buckets'] = get_resource_list(user, user_meta['S3NamingConvention'], user_meta['DataStagingAreas'])
    if user_meta['createGlueDatabases'] == True:
        user_dict['GlueDatabases'] = get_resource_list(user, user_meta['GlueNamingConvention'], user_meta['DataStagingAreas'])
    return user_dict

def read_arguments():
    parser = argparse.ArgumentParser(description='Create Users, S3 buckets and Glue Databases for Customer360 Workshop')
    parser.add_argument('-f', '--file', help='path for JSON file containing users metadata')
    parser.add_argument('-r', '--region', help='Region in which secrets are created', default='eu-west-1')
    parser.add_argument('--delete-s3-buckets', action='store_true', help='Flag to delete all participants S3 buckets')
    parser.add_argument('--delete-glue-databases', action='store_true', help='Flag to delete all participants Glue databases')
    args = parser.parse_args()
    print(args)
    json_arg = vars(args)['file']
    region_arg = vars(args)['region']
    delete_s3 = vars(args)['delete_s3_buckets']
    delete_glue = vars(args)['delete_glue_databases']
    return {'json_path': json_arg, 'region': region_arg, 'delete_s3': delete_s3, 'delete_glue': delete_glue}

def main():
    # Read Arguments
    args = read_arguments()

    # Read JSON
    logger.info('Reading JSON file: %s', args['json_path'])
    users_file = read_users(args['json_path'])
    users = users_file['users']
    users_meta = users_file['userDetails']
    logger.info('Read {:d} users from users filename'.format(len(users)))

    # Parse JSON into List of Dicts
    user_list_full = list(map(lambda x: create_user_dict(x, users_meta), users))

    # Initialize boto3 clients
    secrets_client = boto3.client(
        service_name='secretsmanager',
        region_name=args['region']
    )
    iam_client = boto3.resource('iam')
    s3_client = boto3.client('s3')
    glue_client = boto3.client('glue')

    
    # Create or retrieve existing secrets for AWS Users
    for u in user_list_full:
        logger.info("----------------------------------------------------------------------------------------------")
        logger.info("Customer360: Starting creation of resources for participant: {user}".format(user=u['username']))
        logger.info("----------------------------------------------------------------------------------------------")

        password = SecretsMng.create_secret(secrets_client, u['username'], region_name=args['region'])
        u['password'] = json.loads(password)['password']
        
        logger.info("Customer360: Creating user: {user}".format(user=u['username']))
        logger.info("----------------------------------------------------------------------------------------------")
        
        UserMng.iam_create_user(iam_client, u)
        if args['delete_s3']:
            logger.info("Customer360: Deleting S3 buckets for user: {user}".format(user=u['username']))
            logger.info("----------------------------------------------------------------------------------------------")
            S3Mng.delete_participant_buckets(s3_client, u['username'])
            
        logger.info("Customer360: Creating S3 buckets for user: {user}".format(user=u['username']))
        logger.info("----------------------------------------------------------------------------------------------")
        S3Mng.create_participant_buckets(s3_client, u['S3Buckets'])

        if args['delete_glue']:
            logger.info("Customer360: Deleting Glue databases for user: {user}".format(user=u['username']))
            logger.info("----------------------------------------------------------------------------------------------")
            GlueMng.delete_participant_databases(glue_client, u['username'])

        logger.info("Customer360: Creating Glue Databases for user: {user}".format(user=u['username']))
        logger.info("----------------------------------------------------------------------------------------------")
        GlueMng.create_participant_databases(glue_client, u['GlueDatabases'])

if __name__ == '__main__':
    main()