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


def move_files_to_raw_folder(bucket_name: str, source_folder: str) -> None:
    '''
    Moves files from the current date's folder in the source folder to a new "raw" folder.

    If the "raw" folder doesn't exist, it will be created. If the "raw" folder already exists,
    the files will be copied to the existing folder.

    :param bucket_name: The name of the Amazon S3 bucket.
    :param source_folder: The name of the source folder where the files are located.
    '''
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Get the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Check if the "raw" folder exists
    raw_folder_prefix = f'{source_folder}/raw/{current_date}/'
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=raw_folder_prefix)
    raw_folder_exists = 'Contents' in response

    if not raw_folder_exists:
        # Create the "raw" folder if it doesn't exist
        s3_client.put_object(Bucket=bucket_name, Key=raw_folder_prefix)

    # Define the prefix for the current date's folder
    source_prefix = f'{source_folder}/{current_date}/'

    # List the objects in the bucket based on the prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=source_prefix)

    # Check if any objects are returned
    if 'Contents' in response:
        objects = response['Contents']

        # Move each object to the "raw" folder
        for obj in objects:
            key = obj['Key']
            destination_key = key.replace(source_folder, f'raw/{current_date}')

            # Copy the object to the new location
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': key},
                Key=destination_key
            )

            print(f'Object moved: {key} -> {destination_key}')
    else:
        print('No objects found for the current date.')




# # Configuration
# bucket_name = 'your-bucket'
# source_folder = 'source-folder'

# # Call the function to move the files to the "raw" folder
# move_files_to_raw_folder(bucket_name, source_folder)