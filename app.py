import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to analyze cholesterol levels
def analyze_cholesterol(data):
    if 'chol' not in data.columns:
        st.error("Error: The uploaded file must contain a 'chol' column.")
        return
    
    cholesterol_levels = data['chol'].dropna()

    if cholesterol_levels.empty:
        st.warning("No cholesterol data found in the uploaded file.")
        return

    # Define risk categories
    risk_levels = []
    for value in cholesterol_levels:
        if value < 200:
            risk_levels.append("Normal")
        elif 200 <= value < 240:
            risk_levels.append("Borderline High")
        else:
            risk_levels.append("High Risk")

    # Add classification to DataFrame
    data['Risk Level'] = risk_levels

    # Display results
    st.subheader("📊 Cholesterol Risk Levels")
    st.dataframe(data[['chol', 'Risk Level']].head())

    # Plot distribution
    st.subheader("📈 Cholesterol Level Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(cholesterol_levels, bins=20, kde=True, ax=ax)
    ax.axvline(200, color='yellow', linestyle='dashed', label="Borderline (200 mg/dL)")
    ax.axvline(240, color='red', linestyle='dashed', label="High (240 mg/dL)")
    ax.set_xlabel("Cholesterol Level (mg/dL)")
    ax.set_ylabel("Count")
    ax.legend()
    st.pyplot(fig)

    # Medication suggestions
    st.subheader("💊 Medication Suggestions")
    for risk, level in zip(data['Risk Level'], cholesterol_levels):
        if risk == "Normal":
            st.success(f"Cholesterol Level: {level} mg/dL - No medication needed. Maintain a healthy diet.")
        elif risk == "Borderline High":
            st.warning(f"Cholesterol Level: {level} mg/dL - Consider dietary changes and regular exercise.")
        else:
            st.error(f"Cholesterol Level: {level} mg/dL - Consult a doctor. Medication like statins may be recommended.")

# Streamlit UI
st.title("🩸 Cholesterol Level Monitoring App")
st.write("Upload a CSV file containing cholesterol levels for analysis.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Uploaded Data Preview")
    st.dataframe(df.head())
    analyze_cholesterol(df)
