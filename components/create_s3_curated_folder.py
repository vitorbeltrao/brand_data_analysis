'''
Script to bring raw layer data from s3 to processed, 
performing some transformations

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import os
import logging
import datetime
import boto3
import pandas as pd


def move_files_to_curated_layer(
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str) -> None:
    '''
    Process data from the processed layer, perform additional transformations,
    and save the curated data in the curated layer of the data lake.

    :param bucket_name: (str) Name of the S3 bucket.
    :param aws_access_key_id: (str) AWS access key ID.
    :param aws_secret_access_key: (str) AWS secret access key.
    :param region_name: (str) AWS region name.
    '''
    # Get the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Define the paths for the processed and curated layers
    processed_directory = f'processed/brand-data/atletico/official_page_tweets/extracted_at={current_date}/official_page_tweets.parquet'
    curated_directory = f'curated/brand-data/atletico/official_page_tweets/extracted_at={current_date}/official_page_tweets.csv'

    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create a client instance for S3
    s3_client = session.client('s3')

    # Download the processed data from S3
    s3_client.download_file(bucket_name, processed_directory, 'tmp/processed_data.parquet')

    # Read the processed data from Parquet format
    processed_data = pd.read_parquet('tmp/processed_data.parquet')

    # Perform additional data transformations
    curated_data = processed_data.copy()

    # Create the 'tmp' directory if it doesn't exist
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Save the curated data to parquet format
    curated_data.to_parquet(f'tmp/{current_date}_curated_data.parquet', index=False)

    # Upload the parquet file to S3
    s3_client.upload_file(f'tmp/{current_date}_curated_data.parquet', bucket_name, curated_directory)

    # Delete the temporary files
    os.remove('tmp/processed_data.parquet')
    os.remove(f'tmp/{current_date}_curated_data.parquet')

    logging.info(f'Curated data for {current_date} processed and saved in {curated_directory}.')
