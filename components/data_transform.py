'''
Script to perform some basic data transformations
to feed the database, without mess

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import logging
import uuid
import pandas as pd
import datetime as dt

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def create_auxiliary_columns(transformed_df: pd.DataFrame) -> None:
    '''Function to create three auxiliary columns in datasets:
    "id", "ran_at" and "updated_at"

    :param transformed_df: (dataframe)
    Dataframe after all transformations just
    before being inserted into database
    '''
    # inserting the "id" column with random UUIDs
    transformed_df['id'] = transformed_df.apply(lambda row: hash(uuid.uuid4()) % (10 ** 9), axis=1)
    logging.info(f'Column "id" was inserted: SUCCESS')

    # inserting the "ran_at" and "updated_at" column
    current_time = dt.datetime.now()
    transformed_df['ran_at'] = current_time
    transformed_df['updated_at'] = current_time
    logging.info(
        'Columns "ran_at" and "updated_at" were inserted: SUCCESS')
