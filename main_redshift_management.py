'''
Script to manage the operation of datalake s3

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
import datetime
from decouple import config

from components.create_redshift import create_redshift_table
from components.create_redshift import copy_data_from_s3_to_redshift

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# config
REDSHIFT_HOST = config('REDSHIFT_HOST')
REDSHIFT_PORT = config('REDSHIFT_PORT')
REDSHIFT_DB = config('REDSHIFT_DB')
REDSHIFT_USER = config('REDSHIFT_USER')
REDSHIFT_PASS = config('REDSHIFT_PASS')
BUCKET_NAME = config('BUCKET_NAME')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

# Get today's date
today_date = datetime.datetime.now().date()


if __name__ == "__main__":
    # 1. Creation of the first table curated_official_page_tweets
    logging.info('About to start creating the redshift curated_official_page_tweets table')

    table_name = 'curated_official_page_tweets'
    column_definitions = [
    {'name': 'tweet_id', 'type': 'text'},
    {'name': 'created_at', 'type': 'timestamp'},
    {'name': 'text', 'type': 'text'},
    {'name': 'retweets', 'type': 'integer'},
    {'name': 'likes', 'type': 'integer'},
    {'name': 'id', 'type': 'text'},
    {'name': 'ran_at', 'type': 'timestamp'},
    {'name': 'updated_at', 'type': 'timestamp'},
    {'name': 'year', 'type': 'integer'},
    {'name': 'month', 'type': 'integer'},
    {'name': 'day', 'type': 'integer'},
    {'name': 'hour', 'type': 'integer'},
    {'name': 'day_of_week', 'type': 'integer'}]

    create_redshift_table(REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB, REDSHIFT_USER, REDSHIFT_PASS, table_name, column_definitions)
    logging.info('Finish creating the redshift curated_official_page_tweets table\n')

    # 2. Creation of the first table ngram_one
    logging.info('About to start creating the redshift ngram_one table')

    table_name_ngram_one = 'ngram_one'
    column_definitions_ngram_one = [
        {'name': 'ngrams_1', 'type': 'text'},
        {'name': 'frequencies_1', 'type': 'integer'}]

    create_redshift_table(
        REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB, REDSHIFT_USER, REDSHIFT_PASS, table_name_ngram_one, column_definitions_ngram_one)
    logging.info('Finish creating the redshift ngram_one table\n')

    # 3. copying the data to the table curated_official_page_tweets
    logging.info('About to start uploading data to the curated_official_page_tweets table')

    s3_prefix = f'curated/brand-data/atletico/official_page_tweets/extracted_at=2023-06-06/ngram_one.parquet'
    copy_data_from_s3_to_redshift(
        REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB, REDSHIFT_USER, REDSHIFT_PASS, AWS_ACCESS_KEY_ID, 
        AWS_SECRET_ACCESS_KEY, BUCKET_NAME, s3_prefix, table_name)
    logging.info('Finish uploading data to the curated_official_page_tweets table\n')

    # 4. copying the data to the table ngram_one
    logging.info('About to start uploading data to the ngram_one table')

    s3_prefix_ngram_one = f'curated/brand-data/atletico/official_page_tweets/extracted_at=2023-06-06/ngram_one.parquet'
    copy_data_from_s3_to_redshift(
        REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB, REDSHIFT_USER, REDSHIFT_PASS, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 
        BUCKET_NAME, s3_prefix_ngram_one, table_name_ngram_one)
    logging.info('Finish uploading data to the ngram_one table\n')
