'''
Script to perform some basic data transformations
to feed the database, without mess

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
import pandas as pd
import datetime as dt

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def create_auxiliary_columns(transformed_df: pd.DataFrame) -> None:
    '''Function to create two auxiliary columns in datasets:
    "created_at" and "updated_at"

    :param transformed_df: (dataframe)
    Dataframe after all transformations just
    before being inserted into database
    '''
    # inserting the "updated_at" and "updated_at" column
    current_time = dt.datetime.now()
    transformed_df['created_at'] = current_time
    transformed_df['updated_at'] = current_time
    logging.info(
        'Columns "created_at" and "updated_at" were inserted: SUCCESS')
