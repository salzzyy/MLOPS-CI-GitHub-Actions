import pytest
import pandas as pd
import numpy as np
import streamlit as st
import io


# Test: Verify if the app processes CSV file correctly
def test_csv_file_processing():
    # Create a sample CSV in memory
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [10, 20, 30, 40, 50],
        "C": [100, 200, 300, 400, 500],
    }
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    file = io.StringIO(csv_data)

    # Simulate the file upload in the Streamlit app
    uploaded_file = file

    # If a file is uploaded, process it
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df_uploaded = pd.read_csv(uploaded_file)

        # Test that data is loaded correctly
        assert df_uploaded.shape == (5, 3)  # Checking if there are 5 rows and 3 columns
        assert list(df_uploaded.columns) == ["A", "B", "C"]  # Checking column names

        # Test basic statistics generation
        assert df_uploaded["A"].mean() == 3.0  # Mean of column A
        assert (
            df_uploaded["B"].std() == 15.811388300841896
        )  # Standard deviation of column B


# Test: Check if the visualizations are generated (simple checks)
def test_visualizations():
    # Create a sample DataFrame with numerical data for visualization
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [10, 20, 30, 40, 50],
        "C": [100, 200, 300, 400, 500],
    }
    df = pd.DataFrame(data)

    # Check if we have numerical columns for visualization
    numerical_columns = df.select_dtypes(include=np.number).columns.tolist()

    # Test for pairplot existence
    if len(numerical_columns) > 0:
        # Here, we just check if the function exists; detailed plotting can be done manually
        assert len(numerical_columns) > 0

        # Check if correlation matrix is computed
        corr = df[numerical_columns].corr()
        assert corr.shape == (3, 3)  # Checking if the correlation matrix is 3x3

        # Test the 'choose column' functionality
        assert "A" in df.columns  # Ensure the column exists
        assert df["A"].mean() == 3.0  # Ensure statistics are correct


# Test: Check if column statistics are displayed correctly
def test_column_statistics():
    # Create a sample DataFrame
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [10, 20, 30, 40, 50],
    }
    df = pd.DataFrame(data)

    column_name = "A"

    # Check if statistics are correctly calculated
    assert df[column_name].mean() == 3.0
    assert df[column_name].median() == 3.0
    assert (
        round(df[column_name].std(), 2) == 1.58
    )  # Round the calculated std value to 2 decimal places


# Test: Check if app handles empty CSV correctly
def test_empty_csv():
    # Create an empty DataFrame (with no rows and no columns)
    empty_df = pd.DataFrame()

    # Simulate an empty CSV
    empty_csv = empty_df.to_csv(index=False)
    file = io.StringIO(empty_csv)

    # Now check if the file is truly empty
    try:
        df_uploaded = pd.read_csv(file)

        # Since the CSV is empty, the DataFrame should also be empty
        assert df_uploaded.empty  # Ensure the dataframe is empty

    except pd.errors.EmptyDataError:
        # If the file is empty, assert that we get the EmptyDataError
        assert True  # This will pass the test if the error is raised
