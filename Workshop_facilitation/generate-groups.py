import logging
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
import os
import json
import argparse
import shutil
import pandas as pd

TMP_FOLDER = 'LINK_TEMP'
IP_DICT_JSON_NAME = 'active_ips.json'
GROUP_DICT_NAME = 'groups.json'
GROUP_EXCEL_NAME = 'Groups.xlsx'
AMI_ID = 'ami-060e29600c7769bc0'


def bucket_exists(bucket_name):
    """Determine whether bucket_name exists and the user has permission to access it

    :param bucket_name: string
    :return: True if the referenced bucket_name exists, otherwise False
    """

    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.debug(e)
        return False
    return True


def write_json(d, dest):
    with open(dest, 'w') as cred:
        json.dump(d, cred)


def load_json(dest):
    with open(dest, 'r') as cred:
        return json.load(cred)


def list_ec2():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()

    running_ws_ips = {}

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            if instance['ImageId'] == AMI_ID \
                    and instance['State']['Name'] == 'running':

                running