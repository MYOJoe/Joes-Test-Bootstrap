#!/usr/bin/env python
from __future__ import print_function

import hashlib
import json
import os
import boto3
from six.moves.urllib.request import urlopen

IP_RANGE_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
FUNCTION_ARN = os.environ['FUNCTION_ARN']

def get_lambda_client():
    if os.getenv('ROLE_ARN') is None or os.getenv('ROLE_ARN') == '':
        lambda_client = boto3.client('lambda')
        return lambda_client

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
            )

        lambda_client = role_session.client('lambda')
        return lambda_client

def main():
    md5 = hashlib.md5()
    payload = urlopen(IP_RANGE_URL).read()
    md5.update(payload)
    md5_hex = md5.hexdigest()

    light_sns_notification = json.dumps({
        "Records": [
            {
                "Sns": {
                    "Message": json.dumps({
                        "md5": md5_hex,
                        "url": IP_RANGE_URL
                    })
                }
            }
        ]
    })

    lambda_client = get_lambda_client()
    lambda_client.invoke(
        FunctionName=FUNCTION_ARN,
        Payload=light_sns_notification)

if __name__ == '__main__':
    main()
