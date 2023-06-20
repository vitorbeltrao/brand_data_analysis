'''
Main file that will run all the components in order to
insert the data from the final tables from curated layer
into dw

Author: Vitor Abdo
Date: June/2023
'''

# import necessary packages
import logging
from decouple import config

# data_load component
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
CURATED_TABLE_NAME = config('CURATED_TABLE_NAME')
NGRAM_ONE_TABLE_NAME = config('NGRAM_ONE_TABLE_NAME')
NGRAM_TWO_CURATED_TABLE_NAME = config('NGRAM_TWO_CURATED_TABLE_NAME')
NGRAM_THREE_CURATED_TABLE_NAME = config('NGRAM_THREE_CURATED_TABLE_NAME')


if __name__ == "__main__":
    # 1. create the schema if it does not already exist