import base64
import logging
import json
from logging.config import fileConfig
from botocore.exceptions import ClientError

fileConfig('logging_config.ini')
logger = logging.getLogger()
tags = [{'Key': 'IsWork','Value': 'true'},{'Key': 'WorkType','Value': 'customer360'}]

def get_password(client):
    return client.get_random_password(
    PasswordLength=8,
    ExcludeNumbers=False,
    ExcludePunctuation=True,
    ExcludeUppercase=True,
    ExcludeLowercase=False,
    IncludeSpace=False,
    RequireEachIncludedType=True
)

# Manual forced deletion for secret
# 
# def delete_secret(client):
#     client.restore_secret(
#         SecretId='customer360-username01'
#     )
#     client.delete_secret(
#     SecretId='customer360-username01',
#     ForceDeleteWithoutRecovery=True
# )

def create_secret_string(password, secret_name):
    secret_string = {}
    secret_string['username'] = secret_name
    secret_string['password'] = password['RandomPassword']
    return json.dumps(secret_string)

def create_secret(client, secret_name, region_name='eu-west-1'):
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId='customer360-{username}'.format(username=secret_name)
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Create a new Secret
            password = get_password(client)
            secret_string = create_secret_string(password, secret_name)
            response = client.create_secret(
                Name='customer360-{username}'.format(username=secret_name),
                Description='Secret name for Username: {username}'.format(username=secret_name),
                SecretString=secret_string,
                Tags=tags
            )
            logger.info('Created Secret for {secret_name} with value: {secret_string}'.format(secret_name=secret_name, secret_string=secret_string))
            return response
        else: 
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary']) 
            return decoded_binary_secret
