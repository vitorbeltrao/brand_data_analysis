'''
Streamlit app homepage setup

Author: Vitor Abdo
Date: June/2023
'''

# import necessary packages
import streamlit as st
from PIL import Image

# Define function to load information about the app in the sidebar
def load_about():
    st.sidebar.title("About")
    st.sidebar.info(
        '''
        Questions or suggestions, get in touch:\n📩 vitorbeltrao300@gmail.com
        '''
    )

# Set initial page configurations
st.set_page_config(
    page_title='NASA Asteroids Analysis',
    page_icon='🌌',
)

# Title and image for the app
st.title('Welcome to the NASA Asteroids Analysis App')

# Load and resize the image
image = Image.open('images/nasa-logo-web-rgb.png')  # Replace with the path to your NASA logo

# Display the resized image
st.image(image, use_column_width=True)

# Brief description of the app
st.write('This app allows you to analyze data from the NASA Asteroids Near Earth Object Web Service (AsteroidsNeoWs).')
st.write('You can explore different charts and metrics to gain insights into the asteroids data.')

# Load information about the app in the sidebar
load_about()
