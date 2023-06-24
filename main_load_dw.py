'''
Main file that will run all the components in order to
insert the data from the final tables from processed layer
into dw

Author: Vitor Abdo
Date: June/2023
'''

# import necessary packages
import logging
from decouple import config

from components.get_processed_s3_data import get_files_from_processed_layer
from components.data_load import create_schema_into_postgresql
from components.data_load import create_table_into_postgresql
from components.data_load import insert_data_into_postgresql

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# config
ENDPOINT_NAME = config('ENDPOINT_NAME')
PORT = config('PORT')
DB_NAME = config('DB_NAME')
USER = config('USER')
PASSWORD = config('PASSWORD')
DW_SCHEMA_TO_CREATE = config('DW_SCHEMA_TO_CREATE')
DW_TEMP_SCHEMA_TO_CREATE = config('DW_TEMP_SCHEMA_TO_CREATE')
PROCESSED_TABLE_NAME = config('PROCESSED_TABLE_NAME')
BUCKET_NAME = config('BUCKET_NAME')
SOURCE_DIRECTORY = config('SOURCE_DIRECTORY')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION_NAME = config('REGION_NAME')


if __name__ == "__main__":
    # 1. Get the current processed data
    logging.info('About to start getting data from processed layer')
    processed_data = get_files_from_processed_layer(BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME)
    logging.info('The processed data was obtained successfully\n')

     # 2. create the schema if it does not already exist
    logging.info('About to start executing the create schema function')
    create_schema_into_postgresql(ENDPOINT_NAME, PORT, DB_NAME, USER, PASSWORD, DW_SCHEMA_TO_CREATE) # main schema
    create_schema_into_postgresql(ENDPOINT_NAME, PORT, DB_NAME, USER, PASSWORD, DW_TEMP_SCHEMA_TO_CREATE) # temp schema
    logging.info('Done executing the create schema function\n')

    # 3. create tables
    # 3.1 create first table in "nasa_data_dw" schema
    logging.info(
        'About to start executing the create table "nasa.asteroidsNeows_processed" function')
    table_columns = '''
    id SERIAL PRIMARY KEY,
    name TEXT,
    absolute_magnitude_h FLOAT,
    is_potentially_hazardous_asteroid BOOL,
    is_sentry_object BOOL,
    kilometers_estimated_diameter_min FLOAT,
    kilometers_estimated_diameter_max FLOAT,
    close_approach_date DATETIME,
    orbiting_body TEXT,
    velocity_kilometers_per_hour FLOAT,
    distance_kilometers FLOAT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
    '''

    create_table_into_postgresql(
        ENDPOINT_NAME,
        PORT,
        DB_NAME,
        USER,
        PASSWORD,
        DW_SCHEMA_TO_CREATE,
        PROCESSED_TABLE_NAME,
        table_columns)
    logging.info('Done executing the create table "nasa.asteroidsNeows_processed" function\n')

    # 4. insert transformed dataframes into postgres
    # 4.1 insert data into nasa.asteroidsNeows table
    logging.info('About to start inserting the data into "nasa.asteroidsNeows_processed" table')

    # loading data
    if processed_data.empty:
        logging.info('The dataframe is empty.')
    else:
        insert_data_into_postgresql(
            ENDPOINT_NAME,
            PORT,
            DB_NAME,
            USER,
            PASSWORD,
            DW_SCHEMA_TO_CREATE,
            PROCESSED_TABLE_NAME,
            processed_data,
            DW_TEMP_SCHEMA_TO_CREATE)
        logging.info(
            'Done executing inserting the data into "nasa.asteroidsNeows_processed" table\n')
