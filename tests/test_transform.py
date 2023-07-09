'''
Unit tests for the functions included in
the "data_transform.py" component

Author: Vitor Abdo
Date: July/2023
'''

# import necessary packages
from functions.load_to_rds.components.data_transform import create_auxiliary_columns


def test_create_auxiliary_columns(transformed_df):
    '''Test the create_auxiliary_columns function. This test
    verifies that the create_auxiliary_columns function correctly
    adds the "created_at" and "updated_at" columns to the DataFrame.
    '''
    create_auxiliary_columns(transformed_df)
    assert all(item in transformed_df.columns for item in ['created_at', 'updated_at'])
