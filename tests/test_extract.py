'''
Unit tests for the functions included in
the "data_extract.py" component

Author: Vitor Abdo
Date: July/2023
'''

# import necessary packages
import pandas as pd
import pytest
from functions.load_to_rds.components.data_extract import fetchAsteroidNeowsFeed

@pytest.mark.parametrize(
    'api_key, start_date, end_date',
    [
        ('l16UFmsYlG8gZ6YADf2zsiwKoKw65B0feFtvJfL8', '2023-07-01', '2023-07-07'),
        ('l16UFmsYlG8gZ6YADf2zsiwKoKw65B0feFtvJfL8', '2023-01-01', '2023-01-07'),
        ('l16UFmsYlG8gZ6YADf2zsiwKoKw65B0feFtvJfL8', '2022-12-25', '2023-01-01')
    ]
)


def test_fetchAsteroidNeowsFeed(api_key, start_date, end_date):
    '''Test the fetchAsteroidNeowsFeed function. This test
    verifies that the fetchAsteroidNeowsFeed function correctly
    retrieves asteroid data from the NeoWs API and returns a Pandas DataFrame.
    '''
    df = fetchAsteroidNeowsFeed(api_key, start_date, end_date)
    assert isinstance(df, pd.DataFrame)
