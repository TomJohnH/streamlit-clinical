import streamlit as st
import pandas as pd
import app_def
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from streamlit_timeline import timeline
import plotly.express as px

df = app_def.fetch_data("heart.csv")

st.image("clinical.jpg")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Study report", "Study summary", "Data profile report", "Dataset"]
)

with tab1:

    st.header("Project history")

    with open("timeline_nlp.json", "r") as f:
        data = f.read()
    timeline(data, height=800)

    # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
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

    st.write(
        "The clinical research involved 918 patients with an average age of 53.51. Out of the total patients, 55.34% had heart disease."
    )

    # options = st.multiselect(
    #     "What are your favorite colors",
    #     ["Green", "Yellow", "Red", "Blue"],
    #     ["Yellow", "Red"],
    # )

    # Define min and max ages
    min_age = int(df["Age"].min())
    max_age = int(df["Age"].max())

    # Add slider
    age_range = st.slider("Select age range", min_age, max_age, (min_age, max_age))

    st.write("Below we present histogram of patients age")

    # Filter DataFrame
    filtered_df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]

    # Create histogram
    fig = px.histogram(filtered_df, x="Age")
    st.plotly_chart(fig)

    # Define unique ChestPainType values
    cp_types = df["ChestPainType"].unique()

    # Add multiselect widget
    selected_cp_types = st.multiselect(
        "Select ChestPainType values", cp_types, default=cp_types
    )

    # Filter DataFrame based on selected values
    filtered_df2 = df[df["ChestPainType"].isin(selected_cp_types)]

    # Group data by ChestPainType and HeartDisease, and count the number of occurrences
    counts = (
        filtered_df2.groupby(["ChestPainType", "HeartDisease"])
        .size()
        .reset_index(name="Count")
    )

    # Create bar plot
    fig = px.bar(counts, x="ChestPainType", y="Count", color="HeartDisease")

    # Display plot
    st.plotly_chart(fig)


with tab3:
    if st.button("Run data profile"):
        pr = df.profile_report()
        st_profile_report(pr)

with tab4:
    st.header("Dataset")
    st.write(
        "Data set source: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction?resource=download"
    )

    edited_df = st.experimental_data_editor(df)
