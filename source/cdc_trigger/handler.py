import sys
import os
import re

import json
import boto3
import cr_response

def lambda_handler(event, context):
    
    print(f"Received event:{json.dumps(event)}")
    
    # Create cr_response object
    lambda_response = cr_response.CustomResourceResponse(event)
    cr_params = event['ResourceProperties']
    
    # Validate input
    for key in ['ReplicationTaskArn']:
        if key not in cr_params:
            lambda_response.respond_error(f"{key} property missing")
            return
    
    # Validate input params format
    arn_param = cr_params['ReplicationTaskArn']
    arn_param_match = re.match(r'arn:aws:dms:(.*)', arn_param)
    
    if arn_param_match is None:
        arn_example = "arn:aws:dms:us-east-1:123456789012:task:2PVREMWNPGYJCVU2IBPTOYTIV4"
        arn_format = "arn:aws:dms:<region>:<account>:task:<resourcename>"
        lambda_response.respond_error(f"ReplicationTaskArn must of type {arn_format}. For example: {arn_example}")
        return
    
    # All validations pass. try/expect block to implement logic
    def check_status(status, str):
        return True if status == str else False
    
    try:
        client = boto3.client('dms')
        event['PhysicalResourceId'] = arn_param
        status = client.describe_replication_tasks(Filters=[{'Name':'replication-task-arn', 'Values':[arn_param]}])['ReplicationTasks'][0]['Status']
        
        if event['RequestType'] == 'Create' and  check_status(status.lower(), 'ready'):
            response = client.start_replication_task(ReplicationTaskArn=arn_param, StartReplicationTaskType='start-replication')
            response_data = {k: response['ReplicationTask'][k] for k in response['ReplicationTask'] if k not in ['ReplicationTaskStats']}
            lambda_response.respond(data=response_data)
            return
            
        if event['RequestType'] in ['Delete', 'Update'] and check_status(status.lower(), 'running'):
            response = client.stop_replication_task(ReplicationTaskArn=arn_param)
            response_data = {k: response['ReplicationTask'][k] for k in response['ReplicationTask'] if k not in ['ReplicationTaskStats']}
            lambda_response.respond(data=response_data)
            return
            
        else:
            response_data={}
            lambda_response.respond(data=response_data)   
    
    except Exception as e:
        message = str(e)
        lambda_response.respond_error(message)
        
    return 'OK'

