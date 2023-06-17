'''
Streamlit EDA page

Author: Vitor Abdo
Date: June/2023
'''

# Import necessary packages
import pandas as pd
import numpy as np
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Netflix EDA",
    page_icon="📈"
)

# 1. Title the app
st.title('Data Analysis for Netflix 📈')
st.markdown("**Let's gather some information, insights, and curiosities about Netflix? Let's dive in!** :tv: :bar_chart:")
