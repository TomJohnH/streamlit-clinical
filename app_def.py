import streamlit as st
import pandas as pd


@st.cache_data
def fetch_data(file):
    df = pd.read_csv(file)
    return df
