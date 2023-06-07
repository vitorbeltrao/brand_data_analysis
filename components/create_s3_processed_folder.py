'''
Script to bring raw layer data from s3 to processed, 
performing some transformations

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import boto3
import os
import logging
import datetime
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def move_files_to_processed_layer(
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str) -> None:
    '''
    Process data for the current day from raw layer and save it in the processed layer of the data lake.

    :param bucket_name: (str) Name of the S3 bucket.
    :param aws_access_key_id: (str) AWS access key ID.
    :param aws_secret_access_key: (str) AWS secret access key.
    :param region_name: (str) AWS region name.
    '''
    # Get the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Define the paths for the raw and processed layers
    raw_directory = f'raw/brand-data/atletico/official_page_tweets/extracted_at={current_date}/official_page_tweets.csv'
    processed_directory = f'processed/brand-data/atletico/official_page_tweets/extracted_at={current_date}/processed_data.parquet'

    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create a client instance for S3
    s3_client = session.client('s3')

    # Read the raw data from S3, selecting only desired columns
    obj = s3_client.get_object(Bucket=bucket_name, Key=raw_directory)
    raw_data = pd.read_csv(obj['Body'], names=['tweet_id', 'created_at', 'text', 'retweets', 'likes', 'id', 'ran_at', 'updated_at'])

    # Perform data transformations
    processed_data = raw_data.copy()
    processed_data['created_at'] = pd.to_datetime(processed_data['created_at'])

    # Create the 'tmp' directory if it doesn't exist
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Save the processed data to Parquet format
    processed_data.to_parquet(f'tmp/{current_date}_processed_data.parquet')

    # Upload the Parquet file to S3
    s3_client.upload_file(f'tmp/{current_date}_processed_data.parquet', bucket_name, processed_directory)

    # Delete the temporary file
    os.remove(f'tmp/{current_date}_processed_data.parquet')

    logging.info(f'Processed data for {current_date} processed and saved in {processed_directory}.')
