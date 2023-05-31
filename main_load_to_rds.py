'''
Main file that will run all the components in order to
insert the data from the tables in the database

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
from decouple import config

# data_collector component
from components.extract_tweets import connect_twitter_api
from components.extract_tweets import get_tweets_from_user_for_today

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
# twitter config
CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')
OFFICIAL_TWITTER_USER_ID = config('OFFICIAL_TWITTER_USER_ID')

# RDS database
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
    # 2.1 create first table in "galo_brand_data" schema
    logging.info(
        'About to start executing the create table "official_page_tweets" function')
    table_columns = '''
    tweet_id TEXT,
    created_at TIMESTAMP,
    text TEXT,
    likes INT,
    retweets INT,
    id SERIAL PRIMARY KEY,
    ran_at TIMESTAMP,
    updated_at TIMESTAMP
    '''

    create_table_into_postgresql(
        ENDPOINT_NAME,
        PORT,
        DB_NAME,
        USER,
        PASSWORD,
        SCHEMA_TO_CREATE,
        'official_page_tweets',
        table_columns)
    logging.info('Done executing the create table "official_page_tweets" function\n')

    # 3. insert transformed dataframes into postgres
    # 3.1 insert data into official_page_tweets table
    logging.info('About to start inserting the data into official_page_tweets table')

    # extracting data
    api_connect = connect_twitter_api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN)
    raw_df = get_tweets_from_user_for_today(api_connect, OFFICIAL_TWITTER_USER_ID)

    # transforming data
    create_auxiliary_columns(raw_df) # creating the id, ran_at and updated_at columns

    # loading data
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
        'Done executing inserting the data into official_page_tweets table\n')
