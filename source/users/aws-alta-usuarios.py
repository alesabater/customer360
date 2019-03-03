#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import secrets
import boto3
import string
import argparse
from botocore.exceptions import ClientError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("usernames", help="Comma separated list of users")
    parser.add_argument("groupname", help="Name of the user group to add this(these) user(s) to")
    args = parser.parse_args()

    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|'
    usernames = args.usernames.split(",")
    groupname = args.groupname

    iamres = boto3.resource('iam')

    for username in usernames:
        password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
        print("Username: " + username + "\tPassword: " + password)
        try:
            user = iamres.User(username)
            user.create(
                Path='/'
            )
            response = user.create_login_profile(
                Password=password,
                PasswordResetRequired=True
            )
            if groupname:
                response = user.add_group(
                    GroupName=groupname
                )
            print("User created in group [" + groupname + "]")
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print("User already exists")
            if e.response['Error']['Code'] == 'NoSuchEntity':
                print("Group "+groupname+" does not exist")
            else:
                print("Received error:", e)

if __name__ == "__main__":
    # execute only if run as a script
    main()

#import requests
#apikey="5b417b8cdd6706493e9fe03f42dd576cada57823"
#url='https://onetimesecret.com/api/v1/generate'
#response = requests.post(url,data={'secret':apikey,'ttl':3600},auth=('juan.acevedo@col.vueling.com',apikey))
#response.text
