'''
Script to extract data from twitter
and read them as pandas dataframe

Author: Vitor Abdo
Date: May/2023
'''

# import necessay packages
import datetime
import logging
import pandas as pd
import tweepy as tw

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def connect_twitter_api(
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
        bearer_token: str) -> None:
    '''
    Establishes a connection with the Twitter API using the provided access keys.

    Args:
        consumer_key (str): Consumer Key provided by the Twitter Developer Platform.
        consumer_secret (str): Consumer Secret provided by the Twitter Developer Platform.
        access_token (str): Access Token provided by the Twitter Developer Platform.
        access_token_secret (str): Access Token Secret provided by the Twitter Developer Platform.
        bearer_token (str): Bearer Authentication Token provided by the Twitter Developer Platform.

    Returns:
        tweepy access to use the API
    '''
    permission = tw.OAuthHandler(
        consumer_key,
        consumer_secret)  # Create an authorization handler object using the access keys
    # Set the access information in the authorization object
    permission.set_access_token(access_token, access_token_secret)
    # Create a client using the Bearer Authentication Token
    client = tw.Client(bearer_token=bearer_token)
    # Create an instance of the Twitter API using the authorization object
    api = tw.API(permission)
    logging.info(
        'Twitter API instance using authorization object was created successfully')

    return api

    # Now you can use the "api" variable to make API calls to Twitter and
    # perform operations like getting tweets, sending tweets, etc.


def get_tweets_from_user_for_today(api, user_id):
    '''
    Retrieves tweets from a specific user for the current
    date and returns them as a Pandas DataFrame.

    Args:
        api (tweepy.API): An authenticated instance of the Tweepy API.
        user_id (str or int): The user ID of the specific page from which to retrieve tweets.

    Returns:
        pd.DataFrame: A DataFrame containing the tweet data for the current date, with columns:
                      'tweet_id', 'created_at', 'text', 'likes', 'retweets'.
                      Returns an empty DataFrame if no tweets are found for the current date.
    '''
    # Get today's date
    today_date = datetime.datetime.now().date()

    # List to store the tweet data
    tweet_data = []

    # Retrieve tweets from the specific user
    tweets = api.user_timeline(user_id=user_id, tweet_mode="extended", count=100)
    logging.info('The tweets have been retrieved: SUCCESS')

    # Iterate over the tweets
    for tweet in tweets:
        # Check if the tweet is from today
        if tweet.created_at.date() == today_date:
            # Extract the required tweet data
            tweet_id = tweet.id
            created_at = tweet.created_at
            text = tweet.full_text
            likes = tweet.favorite_count
            retweets = tweet.retweet_count

            # Append the tweet data to the list
            tweet_data.append((tweet_id, created_at, text, likes, retweets))
    logging.info('Tweets have been inserted into a list: SUCCESS')

    # Create a DataFrame from the tweet data
    df_tweets = pd.DataFrame(
        tweet_data,
        columns=[
            'tweet_id',
            'created_at',
            'text',
            'likes',
            'retweets'])
    logging.info('The final dataframe was created: SUCCESS')

    return df_tweets
