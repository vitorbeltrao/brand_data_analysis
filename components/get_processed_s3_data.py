'''
Script to get data from processed layer.

Author: Vitor Abdo
Date: June/2023
'''

# import necessary packages
import boto3
import logging
import datetime
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def get_files_from_processed_layer(
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str) -> pd.DataFrame:
    '''
    Script to get data from processed layer.

    :param bucket_name: (str) Name of the S3 bucket.
    :param aws_access_key_id: (str) AWS access key ID.
    :param aws_secret_access_key: (str) AWS secret access key.
    :param region_name: (str) AWS region name.

    :return processed_data: (pd.DataFrame) data from processed layer in the bucket.
    '''
    # Get the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Define the path for the processed layer
    processed_directory = f'processed/nasa-app/asteroidsNeows/extracted_at={current_date}/processed_asteroidsNeows.parquet'

    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create a client instance for S3
    s3_client = session.client('s3')

    # Read the raw data from S3, selecting only desired columns
    obj = s3_client.get_object(Bucket=bucket_name, Key=processed_directory)
    processed_data = pd.read_csv(obj['Body'], names=[
        'id', 'name', 'absolute_magnitude_h', 'is_potentially_hazardous_asteroid',
        'is_sentry_object', 'kilometers_estimated_diameter_min', 'kilometers_estimated_diameter_max',
        'close_approach_date', 'orbiting_body', 'velocity_kilometers_per_hour', 'distance_kilometers',
        'created_at', 'updated_at'])
    logging.info('The processed data was obtained successfully')
    
    return processed_data
