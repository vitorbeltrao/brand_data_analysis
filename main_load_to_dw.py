'''
Main file that gets data from datalake 
curated layer and goes up to dw

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