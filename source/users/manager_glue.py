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

def delete_participant_bucket(client, db):
    try: 
        logger.info('Deleting Glue Database: [{db}]'.format(db=db))
        response = client.delete_database(Name=db)
        return response
    except ClientError as e:
        logger.info('Unhandled exception when deleting glue database: [{db}]'.format(db=db))
        raise e


def delete_participant_databases(client, user): 
    p = "^{user}_.*_db".format(user=user)
    response = client.get_databases()
    databases = list(map(lambda x: x['Name'], response['DatabaseList']))
    databases_delete = list(filter(None, list(map(lambda x: get_regex_or_none(p, x), databases))))
    databases_str = ", ".join(databases_delete)
    logger.info('Deleting Glue Databases: [{databases}]'.format(databases=databases_str))
    delete_response = list(map(lambda x: delete_participant_bucket(client, x), databases_delete))
    logger.info('Glue Databases deleted successfully')
    return delete_response

def create_participant_database(client, db):
    try: 
        logger.info('Creating Glue Database: [{db}]'.format(db=db))
        response = client.create_database(DatabaseInput={'Name':db})
        response['db_secret'] = {'{db}: SUCCEEDED'.format(db=db)}
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'AlreadyExistsException':
            logger.info('Glue Database: [{db}] Already Exists. Will Skip this step'.format(db=db))
            e.response['db_secret'] = {'{db}: EXISTS'}
            return e.response
        else:
            logger.info('Unhandled exception when creating Glue Database: [{db}]'.format(db=db))
            raise e

def create_participant_databases(client, db_list):
    db_str = ", ".join(db_list)
    logger.info('List of Glue Databases: [{db}]'.format(db=db_str))
    responses = list(map(lambda x: create_participant_database(client, x), db_list))
    logger.info('Databases created successfully')
    return responses





