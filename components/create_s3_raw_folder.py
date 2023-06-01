'''
Script to move data arriving from 
DMS from RDS to raw layer

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import boto3
import logging
import datetime

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def move_files_to_raw_layer(
        bucket_name: str, 
        source_directory: str, 
        aws_access_key_id: str, 
        aws_secret_access_key: str, 
        region_name: str) -> None:
    '''
    Move files from the original directory to the raw layer folder in Amazon S3.

    :param bucket_name: (str) Name of the S3 bucket.
    :param source_directory: (str) Path of the source directory containing the files to be moved.
    :param aws_access_key_id: (str) AWS access key ID.
    :param aws_secret_access_key: (str) AWS secret access key.
    :param region_name: (str) AWS region name.
    '''
    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create a client instance for S3
    s3_client = session.client('s3')

    # Get the file name from the source directory path
    file_name = source_directory.split('/')[-1]

    # Define the destination directory path with the current date
    destination_directory = f'raw/brand-data/atletico/official_page_tweets/extracted_at={datetime.datetime.now().strftime("%Y-%m-%d")}/official_page_tweets.csv'

    # Copy the file to the new directory
    s3_client.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': source_directory},
        Key=destination_directory
    )

    # Delete the file from the original directory
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=source_directory
    )

    logging.info(f'The file {file_name} has been moved to {destination_directory}.')
