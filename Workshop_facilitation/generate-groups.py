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
    :return: True if 