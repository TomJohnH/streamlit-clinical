import streamlit as st
import pandas as pd
import app_def
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from streamlit_timeline import timeline

df = app_def.fetch_data("heart.csv")


tab1, tab2, tab3 = st.tabs(["Study report", "Data profile report", "Dataset"])

with tab1:
    st.image("clinical.jpg")
    st.header("Data metrics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Number of patients", value=len(df.index))
    with col2:
        st.metric(label="Average age", value=f'{df["Age"].mean():.2f}')

    with col3:
        st.metric(
            label="Share of patients with Heart Disease",
            value=f'{df["HeartDisease"].mean():.2%}',
        )
    with open("timeline_nlp.json", "r") as f:
        data = f.read()
    timeline(data, height=800)

    options = st.multiselect(
        "What are your favorite colors",
        ["Green", "Yellow", "Red", "Blue"],
        ["Yellow", "Red"],
    )
    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    if st.button("Run data profile"):
        pr = df.profile_report()
        st_profile_report(pr)

with tab3:
    st.header("Dataset")
    st.write(
        "Data set source: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction?resource=download"
    )

    edited_df = st.experimental_data_editor(df)
