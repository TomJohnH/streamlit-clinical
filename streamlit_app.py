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
    st.subheader("Study summary")
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
    st.subheader("Histograms")
    col1, col2 = st.columns(2)

    with col1:

        st.write("Please select variable and range ")

        # Select only numerical columns
        numerical_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()

        selected_column = st.selectbox("Select a column:", options=numerical_cols)

        # Define min and max ages
        min_var = int(df[selected_column].min())
        max_var = int(df[selected_column].max())

        # Add slider
        var_range = st.slider("Select age range", min_var, max_var, (min_var, max_var))
    with col2:
        st.write("Below we present histogram of patients " + selected_column)

        # Filter DataFrame
        filtered_df = df[
            (df[selected_column] >= var_range[0])
            & (df[selected_column] <= var_range[1])
        ]

        # Create histogram
        fig = px.histogram(filtered_df, x=selected_column)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Type of chest pains vs Heart Disease")
    # Define unique ChestPainType values
    cp_types = df["ChestPainType"].unique()

    # Add multiselect widget
    selected_cp_types = st.multiselect(
        "Select ChestPainType values", cp_types, default=cp_types
    )

    # Filter DataFrame based on selected values
    filtered_df2 = filtered_df[filtered_df["ChestPainType"].isin(selected_cp_types)]

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
    st.write("**Attribute Information**")
    st.write(
        """<ul>
  <li>Age: age of the patient [years]</li>
  <li>Sex: sex of the patient [M: Male, F: Female]</li>
  <li>ChestPainType: chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]</li>
  <li>RestingBP: resting blood pressure [mm Hg]</li>
  <li>Cholesterol: serum cholesterol [mm/dl]</li>
  <li>FastingBS: fasting blood sugar [1: if FastingBS &gt; 120 mg/dl, 0: otherwise]</li>
  <li>RestingECG: resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of &gt; 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]</li>
  <li>MaxHR: maximum heart rate achieved [Numeric value between 60 and 202]</li>
  <li>ExerciseAngina: exercise-induced angina [Y: Yes, N: No]</li>
  <li>Oldpeak: oldpeak = ST [Numeric value measured in depression]</li>
  <li>ST_Slope: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]</li>
  <li>HeartDisease: output class [1: heart disease, 0: Normal]</li>
</ul>""",
        unsafe_allow_html=True,
    )
