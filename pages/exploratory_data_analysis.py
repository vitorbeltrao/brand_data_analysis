'''
Streamlit EDA page

Author: Vitor Abdo
Date: June/2023
'''

# Import necessary packages
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
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
    page_title='NASA Asteroids EDA',
    page_icon='📈'
)

# 1. Title the app
st.title('Data Analysis for NASA Asteroids')
st.subheader("Let's gather some information, insights, and curiosities about NASA Asteroids data? Let's dive in! 🌌")

# 2. Get data from dw
conn_string = f'host={ENDPOINT_NAME} port={PORT} dbname={DB_NAME} user={USER} password={PASSWORD}'
query = '''
    SELECT * FROM nasa_data_dw.nasa_asteroidsneows_processed
    '''
processed_df = fetch_data_from_database(conn_string, query)

# 3. Occasional preprocessing
# 3.1 Passing date column from string to datetime
processed_df['close_approach_date'] = pd.to_datetime(processed_df['close_approach_date'])
processed_df['close_approach_date'] = processed_df['close_approach_date'].dt.date

# 3.2 

# 4. Define function to load information about the app in the sidebar
st.sidebar.title('Filters')
st.sidebar.multiselect(
    'Select an asteroid name:',
    options = processed_df['name'].unique()
)
st.sidebar.multiselect(
    'Select a date:',
    options = processed_df['close_approach_date'].unique()
)

# 5. First block of page dashboard
st.markdown("Let's start by knowing a little about the near-Earth asteroids detected by NASA...")

col1, col2 = st.columns(2)
with col1:
    # 5.1. Lets plot a card
    st.markdown(f'**Number of unique asteroids:** {processed_df.name.nunique()}')

with col2:
    # 5.2. Lets plot a bar graph for asteroids magnitude