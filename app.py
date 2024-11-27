import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the page title
st.title("CSV Data Explorer")

# File uploader to allow the user to upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# If a file is uploaded, process it
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Show a brief overview of the dataset
    st.subheader("Data Overview")
    st.write("Here are the first few rows of your dataset:")
    st.dataframe(df.head())

    # Display basic statistics for numerical columns
    st.subheader("Basic Statistics")
    st.write(df.describe())

    # Show a plot of numerical data if available
    st.subheader("Data Visualization")

    # Check if there are any numerical columns for visualization
    numerical_columns = df.select_dtypes(include=np.number).columns.tolist()

    if len(numerical_columns) > 0:
        # Show a pairplot if there are numerical columns
        st.write("Pairplot of numerical columns:")
        sns.pairplot(df[numerical_columns])
        st.pyplot()  # Display the plot

        # Optionally: Show a correlation heatmap
        st.write("Correlation Heatmap:")
        corr = df[numerical_columns].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        st.pyplot()  # Display the heatmap
    else:
        st.write("No numerical columns found to visualize.")

    # Allow the user to choose a column to display statistics
    column_name = st.selectbox("Choose a column to view its statistics", df.columns)
    st.write(f"Statistics for the column: {column_name}")
    st.write(f"Mean: {df[column_name].mean()}")
    st.write(f"Median: {df[column_name].median()}")
    st.write(f"Standard Deviation: {df[column_name].std()}")

# Footer with additional information
st.write(
    "This is a simple Streamlit app that allows you to upload CSV files and explore the data using basic statistics and visualizations."
)
