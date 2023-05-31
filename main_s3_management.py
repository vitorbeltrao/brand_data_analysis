'''
Script to manage the operation of datalake s3

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
from decouple import config

from components.create_s3_raw_folder import move_files_to_daily_directory

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# config
BUCKET_NAME = config('BUCKET_NAME')
SOURCE_DIRECTORY = config('SOURCE_DIRECTORY')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION_NAME = config('REGION_NAME')


if __name__ == "__main__":
    logging.info('About to start moving the data from staging to raw bucket')
    move_files_to_daily_directory(
        BUCKET_NAME, SOURCE_DIRECTORY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME)
    logging.info('Finish moving the data from staging to raw bucket')
