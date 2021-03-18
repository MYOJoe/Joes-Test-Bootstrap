#!/usr/bin/env python
from __future__ import print_function

import os
import boto3

FUNCTION_ARN = os.environ['FUNCTION_ARN']

def get_sns_client():
    if os.getenv('ROLE_ARN') is None or os.getenv('ROLE_ARN') == '':
        sns_client = boto3.client('sns', region_name='us-east-1')
        return sns_client

    else:
        sts_client = boto3.client('sts')
        credentials = sts_client.assume_role(
                RoleArn=os.environ['ROLE_ARN'],
                RoleSessionName='InvokeFunction'
            )

        role_session = boto3.Session(
                aws_access_key_id=credentials['Credentials']['AccessKeyId'],
                aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
                aws_session_token=credentials['Credentials']['SessionToken'],
                region_name='us-east-1'
            )

        sns_client = role_session.client('sns')
        return sns_client

def main():
    sns_client = get_sns_client()
    paginator = sns_client.get_paginator('list_subscriptions')
    pages = paginator.paginate()

    for subscriptions in pages:
        for subscription in subscriptions['Subscriptions']:
            if subscription['Endpoint'] == FUNCTION_ARN:
                sns_client.unsubscribe(
                    SubscriptionArn=subscription['SubscriptionArn']
                )
                print('Unsubscribed: ' + subscription['Endpoint'])

if __name__ == '__main__':
    main()
