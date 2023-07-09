'''
This .py file is for creating the fixtures

Author: Vitor Abdo
Date: July/2023
'''

# import necessary packages
import pytest
import pandas as pd


@pytest.fixture
def transformed_df():
    # Create a sample transformed DataFrame
    data = {
        'id': [1, 2, 3],
        'name': ['John', 'Jane', 'Bob'],
        'age': [30, 25, 40]
    }
    df = pd.DataFrame(data)
    return df
