'''
Main file that will run all the components in order to
insert the data from the tables in the database

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
from decouple import config
from datetime import datetime, timedelta

# data_collector component
from components.data_extract import fetchAsteroidNeowsFeed

# data_transform component
from components.data_transform import create_auxiliary_columns

# data_load component
from components.data_load import create_schema_into_postgresql
from components.data_load import create_table_into_postgresql
from components.data_load import insert_data_into_postgresql

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# config
NASA_API_KEY = config('NASA_API_KEY')
ENDPOINT_NAME = config('ENDPOINT_NAME')
PORT = config('PORT')
DB_NAME = config('DB_NAME')
USER = config('USER')
PASSWORD = config('PASSWORD')
SCHEMA_TO_CREATE = config('SCHEMA_TO_CREATE')
TEMP_SCHEMA_TO_CREATE = config('TEMP_SCHEMA_TO_CREATE')
TABLE_NAME = config('TABLE_NAME')


if __name__ == "__main__":
    # 1. create the schema if it does not already exist
    logging.info('About to start executing the create schema function')
    create_schema_into_postgresql(ENDPOINT_NAME, PORT, DB_NAME, USER, PASSWORD, SCHEMA_TO_CREATE) # main schema
    create_schema_into_postgresql(ENDPOINT_NAME, PORT, DB_NAME, USER, PASSWORD, TEMP_SCHEMA_TO_CREATE) # temp schema
    logging.info('Done executing the create schema function\n')

    # 2. create tables
    # 2.1 create first table in "nasa_data_db" schema
    logging.info(
        'About to start executing the create table "nasa.asteroidsNeows" function')
    table_columns = '''
    links TEXT,
    id SERIAL PRIMARY KEY,
    neo_reference_id TEXT,
    name TEXT,
    nasa_jpl_url TEXT,
    absolute_magnitude_h FLOAT,
    estimated_diameter TEXT,
    is_potentially_hazardous_asteroid BOOL,
    close_approach_data TEXT,
    is_sentry_object BOOL 
    created_at TIMESTAMP,
    updated_at TIMESTAMP
    '''

    create_table_into_postgresql(
        ENDPOINT_NAME,
        PORT,
        DB_NAME,
        USER,
        PASSWORD,
        SCHEMA_TO_CREATE,
        TABLE_NAME,
        table_columns)
    logging.info('Done executing the create table "nasa.asteroidsNeows" function\n')

    # 3. insert transformed dataframes into postgres
    # 3.1 insert data into nasa.asteroidsNeows table
    logging.info('About to start inserting the data into "nasa.asteroidsNeows" table')

    # extracting data
    today_date = datetime.now().date()
    date_seven_days_ago = today_date - timedelta(days=7)
    raw_df = fetchAsteroidNeowsFeed(NASA_API_KEY, date_seven_days_ago, today_date)
    logging.info(f'Data from {date_seven_days_ago} to {today_date} extracted successfully')
 
    # transforming data
    create_auxiliary_columns(raw_df) # creating the created_at and updated_at columns

    # loading data
    if raw_df.empty:
        logging.info('The dataframe is empty.')
    else:
        insert_data_into_postgresql(
            ENDPOINT_NAME,
            PORT,
            DB_NAME,
            USER,
            PASSWORD,
            SCHEMA_TO_CREATE,
            TABLE_NAME,
            raw_df,
            TEMP_SCHEMA_TO_CREATE)
        logging.info(
            'Done executing inserting the data into "nasa.asteroidsNeows" table\n')
