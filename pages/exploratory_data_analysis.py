'''
Streamlit EDA page

Author: Vitor Abdo
Date: June/2023
'''

# Import necessary packages
import pandas as pd
import streamlit as st
import plotly.express as px
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

# 3.2 Select the top five magnitudes
top_five_magnitudes = processed_df.sort_values(by=['absolute_magnitude_h'], ascending=False).head(5)

# 3.3 Groupby comparing the dangerous and non dangerous asteroids
grouped = processed_df.groupby('is_potentially_hazardous_asteroid')
grouped = grouped[['kilometers_estimated_diameter_min', 
                   'kilometers_estimated_diameter_max', 
                   'velocity_kilometers_per_hour']].agg(['mean', 'median', 'std'])

# 3.4 Select the top five distances from earth
top_five_distances = processed_df.sort_values(by=['distance_kilometers'], ascending=True).head(5)

# 3.5 Select only PHA
pha_df = processed_df.loc[(processed_df['is_potentially_hazardous_asteroid']) == True].reset_index(drop=True)
pha_df = pha_df[['name', 'absolute_magnitude_h', 'kilometers_estimated_diameter_min',
                 'kilometers_estimated_diameter_max', 'velocity_kilometers_per_hour',
                 'distance_kilometers']]

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
    # 5.1. Lets plot a scatter plot
    diameters_scatter_plot = px.scatter(
    processed_df, x='kilometers_estimated_diameter_min', y='kilometers_estimated_diameter_max', orientation='v', 
    title='Minimum vs maximum diameter of asteroids',  
    labels={
        'kilometers_estimated_diameter_min': 'Estimated min. diameter (Km)',
        'kilometers_estimated_diameter_max': 'Estimated max. diameter (Km)'})
    st.plotly_chart(diameters_scatter_plot, use_container_width=True)

with col2:
    # 5.2. Lets plot a bar graph for asteroids magnitude
    magnitude_bar_chart = px.bar(
        top_five_magnitudes, x='name', y='absolute_magnitude_h', orientation='v', 
        title='Five largest magnitudes of asteroids',  
        labels={
            'name': 'Asteroid name',
            'absolute_magnitude_h': 'Absolute magnitude (au)'})
    st.plotly_chart(magnitude_bar_chart, use_container_width=True)

# 6. Second block of page dashboard
st.markdown("Now, let's see how dangerous these asteroids are with regards to colliding with earth and their technical characteristics.")
st.markdown('#') # white space in dashboard

# 6.1. Lets plot a table
st.markdown('**Table comparing statistics of potentially hazardous (True) and non-hazardous (False) asteroids**')
st.table(grouped.T)
st.markdown('We can see that the mean and median of the variables for potentially hazardous asteroids are larger than non-hazardous ones. Makes sense, right?')

# 7. Third block of page dashboard
st.markdown('And how close will they be from Earth?')

# 7.1. Lets plot a bar graph for asteroids distances
distance_bar_chart = px.bar(
    top_five_distances, x='name', y='distance_kilometers', orientation='v', color='is_potentially_hazardous_asteroid', 
    title='The five closest asteroids to Earth',  
    labels={
        'name': 'Asteroid name',
        'distance_kilometers': 'Distance (Km)',
        'is_potentially_hazardous_asteroid': 'Is potentially hazardous'})
st.plotly_chart(distance_bar_chart, use_container_width=True)

st.markdown(
    '''
    The closest is approximately 4 million kilometers away, 
    for our dimensions as humans, it doesn't seem that close, right? 
    But to be classified as a PHA, an asteroid must have a minimum 
    orbit intersection distance of less than 0.05 astronomical units 
    (equivalent to 7.5 million km), plus other features.
    ''')

# 8. Fourth block of page dashboard
st.markdown("Continuing on this topic, let's see a table of potentially dangerous asteroids and their characteristics?")
st.table(pha_df.T)

# 9. Fifth block of page dashboard
st.markdown("That's it for now, let's finish with some curiosities...")

# 9.1. Number of unique asteroids
st.markdown(f'**Number of unique asteroids:** {processed_df.name.nunique()}')

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'**Smallest diameter of an asteroid:** {round(processed_df.kilometers_estimated_diameter_min.min(), 3)} Km')
    st.markdown(f'**Lowest velocity of an asteroid:** {round(processed_df.velocity_kilometers_per_hour.min(), 2)} Km/h')
    
with col2:
    st.markdown(f'**Biggest diameter of an asteroid:** {round(processed_df.kilometers_estimated_diameter_max.max(), 2)} Km')
    st.markdown(f'**Faster velocity of an asteroid:** {round(processed_df.velocity_kilometers_per_hour.max(), 2)} Km/h')
