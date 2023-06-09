'''
Script to manage the operation of datalake s3

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
import boto3
from decouple import config

from components.create_s3_raw_folder import move_files_to_raw_layer
from components.create_s3_processed_folder import move_files_to_processed_layer

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# config
BUCKET_NAME = config('BUCKET_NAME')
SOURCE_DIRECTORY = config('SOURCE_DIRECTORY')
AWS_ACCESSKEYID = config('AWS_ACCESSKEYID')
AWS_SECRETACCESSKEY = config('AWS_SECRETACCESSKEY')
REGION_NAME = config('REGION_NAME')

# Create a session with AWS credentials
session = boto3.Session(
    aws_access_key_id=AWS_ACCESSKEYID,
    aws_secret_access_key=AWS_SECRETACCESSKEY,
    region_name=REGION_NAME
)

 # Create a client instance for S3
s3_client = session.client('s3')


def lambda_handler(event, context):
    # 1. Move data from staging to RAW
    logging.info('About to start moving the data from staging to raw bucket')
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=SOURCE_DIRECTORY)
        csv_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].lower().endswith('.csv')]

        for file in csv_files:
            move_files_to_raw_layer(
                BUCKET_NAME, file, AWS_ACCESSKEYID, AWS_SECRETACCESSKEY, REGION_NAME)
    except:
        logging.info('Staging folder is empty')

    logging.info('Finish moving the data from staging to raw bucket\n')

    # 2. Move data from RAW to PROCESSED
    logging.info('About to start moving the data from raw to processed layer')
    move_files_to_processed_layer(BUCKET_NAME, AWS_ACCESSKEYID, AWS_SECRETACCESSKEY, REGION_NAME)
    logging.info('Finish moving the data from raw to processed layer\n')
