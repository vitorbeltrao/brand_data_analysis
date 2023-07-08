'''
Script to bring raw layer data from s3 to processed, 
performing some transformations

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import boto3
import json
import os
import logging
import datetime
import pandas as pd
import io

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
    raw_directory = f'raw/nasa-app/asteroidsNeows/extracted_at={current_date}/asteroidsNeows.csv'
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
    obj = s3_client.get_object(Bucket=bucket_name, Key=raw_directory)
    raw_data = pd.read_csv(obj['Body'], names=['links', 'id', 'neo_reference_id', 'name', 'nasa_jpl_url', 
                                               'absolute_magnitude_h', 'estimated_diameter', 'is_potentially_hazardous_asteroid',
                                               'close_approach_data', 'is_sentry_object', 'created_at', 'updated_at'])

    ######################### Perform data transformations #########################
    processed_data = raw_data.copy()
    processed_data.drop(['links', 'neo_reference_id', 'nasa_jpl_url'], axis=1, inplace=True) # drop unnecessary columns
    processed_data['name'] = processed_data['name'].str.replace(r'\(|\)', '', regex=True) # remove unnecessary parentesis of instances
    logging.info('Columns have been removed: SUCCESS')

    # normalize 'estimated_diameter' column
    processed_data['estimated_diameter'] = processed_data['estimated_diameter'].apply(json.loads)
    diameter = pd.json_normalize(processed_data['estimated_diameter'])
    diameter = diameter[['kilometers.estimated_diameter_min', 'kilometers.estimated_diameter_max']]
    diameter.rename(columns = {
        'kilometers.estimated_diameter_min':'kilometers_estimated_diameter_min',
        'kilometers.estimated_diameter_max':'kilometers_estimated_diameter_max'}, inplace = True)
    logging.info('Column "estimated_diameter" have been normalized: SUCCESS')

    # normalize 'close_approach_data' column
    close_approach_slice_one = pd.DataFrame()
    processed_data['close_approach_data'] = processed_data['close_approach_data'].apply(json.loads)

    for item in processed_data['close_approach_data']:
        df_item = pd.DataFrame(item, index=[0]) # Creates a DataFrame for each list item
        close_approach_slice_one = pd.concat([close_approach_slice_one, df_item], ignore_index=True) # Concatenates the DataFrame to the result

    close_approach_slice_two = pd.json_normalize(close_approach_slice_one['relative_velocity'])
    close_approach_slice_three = pd.json_normalize(close_approach_slice_one['miss_distance'])

    slice_one_two = close_approach_slice_one.join(close_approach_slice_two)
    close_approach_final = slice_one_two.join(close_approach_slice_three)

    close_approach_final = close_approach_final[
        ['close_approach_date', 'orbiting_body', 
         'kilometers_per_hour', 'kilometers']]
    
    close_approach_final.rename(columns = {
        'kilometers_per_hour':'velocity_kilometers_per_hour',
        'kilometers':'distance_kilometers'}, inplace = True)
    logging.info('Column "close_approach_data" have been normalized: SUCCESS')
    
    # join everything in one final dataframe and do final modifications
    processed_data.reset_index(inplace=True, drop=True)

    processed_data_intermediate = processed_data.join(diameter)
    processed_data_final = processed_data_intermediate.join(close_approach_final)
    processed_data_final.drop(['estimated_diameter', 'close_approach_data'], axis=1, inplace=True)

    processed_data_final['close_approach_date'] = pd.to_datetime(processed_data_final['close_approach_date'])
    processed_data_final['velocity_kilometers_per_hour'] = processed_data_final['velocity_kilometers_per_hour'].astype(float)
    processed_data_final['distance_kilometers'] = processed_data_final['distance_kilometers'].astype(float)

    logging.info('All dataframes with transformations have been merged: SUCCESS')
    ####################################################################################################
    # Create the 'tmp' directory if it doesn't exist
    # if not os.path.exists('tmp'):
    #     os.makedirs('tmp')

    # Converta o DataFrame em um arquivo Parquet em memória
    parquet_buffer = io.BytesIO()
    processed_data_final.to_parquet(parquet_buffer)
    parquet_buffer.seek(0)

    # Faça o upload do arquivo Parquet diretamente para o S3
    s3_client.upload_fileobj(parquet_buffer, bucket_name, processed_directory)

    # # Upload the Parquet file to S3
    # s3_client.upload_file(f'/tmp/{current_date}_processed_asteroidsNeows.parquet', bucket_name, processed_directory)

    # Delete the temporary file
    os.remove(f'/tmp/{current_date}_processed_asteroidsNeows.parquet')
    logging.info(f'Processed data for {current_date} processed and saved in {processed_directory}.')
