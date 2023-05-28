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
    '''Function to create three auxiliary columns in datasets:
    "id", "created_at" and "updated_at"

    :param transformed_df: (dataframe)
    Dataframe after all transformations just
    before being inserted into database
    '''
    # inserting the "id" column
    transformed_df['id'] = pd.Series(range(1, len(transformed_df) + 1))
    logging.info(f'Column "id" was inserted: SUCCESS')

    # inserting the "created_at" and "updated_at" column
    transformed_df['created_at'] = dt.datetime.now()
    transformed_df['updated_at'] = transformed_df['created_at']
    logging.info(
        'Columns "created_at" and "updated_at" was inserted: SUCCESS')
