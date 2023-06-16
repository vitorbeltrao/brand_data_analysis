'''
Script to manage the functions to upload data 
from the curated layer from datalake to dw

Author: Vitor Abdo
Date: June/2023
'''

# import necessary packages
import os
import boto3
import pandas as pd
from datetime import datetime

from decouple import config

# Configuração do AWS S3
s3_bucket_name = 'brand-data-cf-mys3bucket-11lvsw0kmdkxu'
s3_prefix = 'curated/brand-data/atletico/official_page_tweets'
s3_data_location = f's3://{s3_bucket_name}/{s3_prefix}'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION_NAME = config('REGION_NAME')

def list_parquet_files_in_s3(
        aws_access_key_id: str, 
        aws_secret_access_key: str, 
        region_name: str, 
        s3_bucket_name: str, 
        s3_location: str) -> str:
    '''
    Lists the .parquet files in the specified S3 location.

    Args:
        s3_location (str): The S3 location to search for .parquet files.

    Returns:
        List[str]: A list of .parquet file paths.
    '''
    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name)

    s3_client = session.client('s3')
    s3_resource = session.resource('s3')
    my_bucket = s3_resource.Bucket(s3_bucket_name)

    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object.key)




def load_parquet_file_from_s3(
        aws_access_key_id: str, 
        aws_secret_access_key: str, 
        region_name: str,
        s3_bucket_name: str, 
        s3_file_path: str) -> pd.DataFrame:
    '''
    Loads a .parquet file from the specified S3 path into a DataFrame.

    Args:
        s3_file_path (str): The S3 path of the .parquet file.

    Returns:
        pandas.DataFrame: The DataFrame containing the data from the .parquet file.
    '''
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    s3_client = session.client('s3')
    response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_file_path)
    df = pd.read_parquet(response['Body'])

    return df


current_date = datetime.now().strftime('%Y-%m-%d')
s3_data_location_today = s3_data_location.replace('{data_do_dia}', current_date)

parquet_files = list_parquet_files_in_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, s3_bucket_name, s3_data_location)

# Loop para processar cada arquivo .parquet e inserir os dados no banco de dados
for parquet_file in parquet_files:
    s3_file_path = f's3://{s3_bucket_name}/{parquet_file}'

    # Carrega o arquivo .parquet como DataFrame
    df = load_parquet_file_from_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, s3_bucket_name, s3_file_path)