'''
Streamlit EDA page

Author: Vitor Abdo
Date: June/2023
'''

# Import necessary packages
import pandas as pd
import numpy as np
import streamlit as st
from decouple import config

from components.data_extract import fetch_data_from_database

# config
ENDPOINT_NAME = config('ENDPOINT_NAME')
PORT = config('PORT')
DB_NAME = config('DB_NAME')
USER = config('USER')
PASSWORD = config('PASSWORD')

# Set page config
st.set_page_config(
    page_title="NASA Asteroids EDA",
    page_icon="📈"
)

# 1. Title the app
st.title('Data Analysis for NASA Asteroids 📈')
st.markdown("**Let's gather some information, insights, and curiosities about NASA Asteroids data? Let's dive in!** 🌌")

# 2. Define function to load information about the app in the sidebar
st.sidebar.title("Filters")



# 2. Get data from dw
conn_string = f"host={ENDPOINT_NAME} port={PORT} dbname={DB_NAME} user={USER} password={PASSWORD}"
query = '''
    SELECT * FROM nasa_data_dw.nasa_asteroidsneows_processed
    '''
processed_df = fetch_data_from_database(conn_string, query)

# 3. Read the data in strealit
st.dataframe(processed_df)
