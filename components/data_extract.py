'''
Script to extract data from nasa API
and database

Author: Vitor Abdo
Date: May/2023
'''

# import necessay packages
import requests
import pandas as pd
import logging
import pyodbc

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def fetchAsteroidNeowsFeed(api_key: str, start_date: str, end_date: str) -> pd.DataFrame:
    '''
    Retrieves asteroid data from NASA's NeoWs API and returns a Pandas DataFrame.

    Parameters:
        - api_key (str): NASA API key.
        - start_date (str): Start date for retrieving asteroid data (in 'YYYY-MM-DD' format).
        - end_date (str): End date for retrieving asteroid data (in 'YYYY-MM-DD' format).

    Returns:
        - Pandas DataFrame containing the asteroid data.
    '''
    URL_NeoFeed = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key
    }

    try:
        logging.info("Making request to NeoWs API...")
        response = requests.get(URL_NeoFeed, params=params)

        if response.status_code == 200:
            logging.info("Request successful. Converting data to DataFrame...")

            # Extract asteroid data from the response
            data = response.json()
            asteroids = []
            for date in data['near_earth_objects'].keys():
                asteroids.extend(data['near_earth_objects'][date])

            # Create a Pandas DataFrame with the asteroid data
            df = pd.DataFrame(asteroids)

            logging.info("Conversion completed. DataFrame created successfully.")
            return df
        else:
            logging.error("Request failed. Status code: %d", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        logging.error("Error during API request: %s", str(e))
        return None
    

def fetch_data_from_database(conn_string: str, query: str) -> pd.DataFrame:
    '''
    Fetches data from a database using the provided connection string and query.

    Parameters:
        conn_string (str): Connection string for the database.
        query (str): SQL query to fetch the data.

    Returns:
        DataFrame: A DataFrame containing the fetched data.
    '''
    conn = None  # Definir a variável 'conn' como None

    try:
        # Connect to the database
        conn = pyodbc.connect(conn_string)

        # Fetch the data using the query
        logging.info('Fetching data from the database...')
        data = pd.read_sql(query, conn)

    except Exception as e:
        logging.error(f'Error fetching data from the database: {str(e)}')
        raise
    finally:
        # Close the connection if it was successfully established
        if conn is not None:
            conn.close()

    return data
