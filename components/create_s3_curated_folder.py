'''
Script to bring raw layer data from s3 to processed, 
performing some transformations

Author: Vitor Abdo
Date: May/2023
'''

# import necessary packages
import os
import logging
import datetime
import boto3
import pandas as pd
import re
import string

import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')


def extract_ngrams(text, n):
    '''
    Extracts n-grams from a given text.

    Args:
        text (str): The text to extract n-grams from.
        n (int): The size of the n-grams.

    Returns:
        list: A list of n-grams extracted from the text.
    '''
    tokens = word_tokenize(text.lower())  # Tokenization
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]  # Remove stopwords
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]  # Lemmatize tokens
    
    n_grams = ngrams(lemmatized_tokens, n)  # Extract n-grams
    return [' '.join(grams) for grams in n_grams]


def clean_text(text):
    '''
    Cleans the text by converting it to lowercase, removing square brackets, links, punctuation,
    and words containing numbers.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    '''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text) # Remove the urls
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) # Remove the punctuation
    text = re.sub('\n', '',text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def get_ngram_frequencies(df, column, n):
    '''
    Extracts n-grams from a column of a DataFrame and calculates their frequencies.

    Args:
        df (pandas.DataFrame): The DataFrame containing the text column.
        column (str): The name of the text column in the DataFrame.
        n (int): The size of the n-grams.

    Returns:
        pandas.DataFrame: A DataFrame with columns for n-grams and their frequencies.
    '''
    ngrams_freq = Counter()
    for text in df[column]:
        cleaned_text = clean_text(text)
        ngrams = extract_ngrams(cleaned_text, n)
        ngrams_freq.update(ngrams)
    
    ngrams_list = []
    freq_list = []
    for ngram, freq in ngrams_freq.items():
        ngrams_list.append(ngram)
        freq_list.append(freq)
    
    new_df = pd.DataFrame()
    new_df[f'ngrams_{n}'] = ngrams_list
    new_df[f'frequencies_{n}'] = freq_list
    
    return new_df


def move_files_to_curated_layer(
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str) -> None:
    '''
    Process data from the processed layer, perform additional transformations,
    and save the curated data in the curated layer of the data lake.

    :param bucket_name: (str) Name of the S3 bucket.
    :param aws_access_key_id: (str) AWS access key ID.
    :param aws_secret_access_key: (str) AWS secret access key.
    :param region_name: (str) AWS region name.
    '''
    # Get the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Define the paths for the processed and curated layers
    processed_directory = f'processed/brand-data/netflix/extracted_at={current_date}/processed_data.parquet'
    curated_directory = f'curated/brand-data/netflix/extracted_at={current_date}/'

    # Create a session with AWS credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Create a client instance for S3
    s3_client = session.client('s3')

    # Download the processed data from S3
    processed_file_path = 'tmp/processed_data.parquet'
    s3_client.download_file(bucket_name, processed_directory, processed_file_path)

    # Read the processed data from Parquet format
    processed_data = pd.read_parquet(processed_file_path)

    # Perform additional data transformations
    curated_data = processed_data.copy()

    curated_data['year'] = curated_data.created_at.dt.year
    curated_data['month'] = curated_data.created_at.dt.month
    curated_data['day'] = curated_data.created_at.dt.day
    curated_data['hour'] = curated_data.created_at.dt.hour
    curated_data['day_of_week'] = curated_data.created_at.dt.dayofweek

    ngram_one = get_ngram_frequencies(curated_data, 'text', 1)
    ngram_two = get_ngram_frequencies(curated_data, 'text', 2)
    ngram_three = get_ngram_frequencies(curated_data, 'text', 3)

    # Create the 'tmp' directory if it doesn't exist
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Save the curated data and ngrams to temporary files
    curated_data_file = 'curated_data.parquet'
    ngram_one_file = 'ngram_one.parquet'
    ngram_two_file = 'ngram_two.parquet'
    ngram_three_file = 'ngram_three.parquet'

    curated_data.to_parquet(f'tmp/{curated_data_file}', index=False)
    ngram_one.to_parquet(f'tmp/{ngram_one_file}', index=False)
    ngram_two.to_parquet(f'tmp/{ngram_two_file}', index=False)
    ngram_three.to_parquet(f'tmp/{ngram_three_file}', index=False)

    # Upload the curated data and ngrams to S3
    s3_client.upload_file(f'tmp/{curated_data_file}', bucket_name, curated_directory + curated_data_file)
    s3_client.upload_file(f'tmp/{ngram_one_file}', bucket_name, curated_directory + ngram_one_file)
    s3_client.upload_file(f'tmp/{ngram_two_file}', bucket_name, curated_directory + ngram_two_file)
    s3_client.upload_file(f'tmp/{ngram_three_file}', bucket_name, curated_directory + ngram_three_file)

    # # Delete the temporary files
    # os.remove(processed_file_path)
    # os.remove(f'tmp/{curated_data_file}')
    # os.remove(f'tmp/{ngram_one_file}')
    # os.remove(f'tmp/{ngram_two_file}')
    # os.remove(f'tmp/{ngram_three_file}')

    # Log the successful completion
    logging.info(f'Curated data for {current_date} processed and saved in {curated_directory}.')
