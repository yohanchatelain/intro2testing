import os
import subprocess

import numpy as np
import pandas as pd
from best_science_ever.best_science_ever import concat, process, split


def remove_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


def test_split():
    """Test the split function."""
    df = pd.DataFrame(np.random.rand(100, 5))  # Create a random dataframe
    split_dfs = split(df, 10)
    assert len(split_dfs) == 10  # Check if it correctly splits into 10 dataframes
    for s_df in split_dfs:
        assert len(s_df) == 10  # Check if each split dataframe has 10 rows


def test_process():
    """Test the process function."""
    df = pd.DataFrame(np.random.rand(10, 5))  # Create a random dataframe
    processed_df = process(df)
    assert "mean" in processed_df.columns  # Check if 'mean' column is added
    for idx, row in processed_df.iterrows():
        assert row["mean"] == np.mean(row[:-1])  # Check if mean is calculated correctly


def test_concat():
    """Test the concat function."""
    dfs = [
        pd.DataFrame(np.random.rand(10, 5)) for _ in range(3)
    ]  # Create 3 random dataframes
    concatenated_df = concat(dfs)
    assert (
        len(concatenated_df) == 30
    )  # Check if the concatenated dataframe has correct number of rows


def test_cli_split():
    """Test the CLI behavior for 'split' mode."""
    # Create a sample dataframe and save it as a CSV file for testing
    test_df = pd.DataFrame({"A": range(50), "B": range(50, 100)})
    test_filename = "test_data_df.csv"
    test_df.to_csv(test_filename, index=False)

    # Run the script with the 'split' mode
    subprocess.run(
        ["best_science_ever", "split", test_filename, "--n_rows", "10"],
        check=True,
    )

    # Check if the split files are created correctly
    for i in range(5):  # Expecting 5 files because 50 rows split into groups of 10
        split_filename = f"test_data_df_{i}_processed.csv"
        assert os.path.exists(
            split_filename
        ), f"Split file {split_filename} does not exist"
        split_df = pd.read_csv(split_filename)
        assert (
            len(split_df) == 10
        ), f"Split file {split_filename} does not have expected row count"

    # Cleanup - remove created files
    remove_file(test_filename)
    for i in range(5):
        remove_file(f"test_data_df_{i}_processed.csv")


def test_cli_process():
    """Test the CLI behavior for 'process' mode."""
    # Create a sample dataframe and save it as a CSV file for testing
    test_df = pd.DataFrame({"A": range(50), "B": range(50, 100)})
    test_filename = "test_data_df.csv"
    test_df.to_csv(test_filename, index=False)

    # Run the script with the 'process' mode
    subprocess.run(
        ["best_science_ever", "process", test_filename],
        check=True,
    )

    # Check if the processed file is created correctly
    processed_filename = "test_data_df_processed.csv"
    assert os.path.exists(
        processed_filename
    ), f"Processed file {processed_filename} does not exist"
    processed_df = pd.read_csv(processed_filename)
    assert (
        len(processed_df) == 50
    ), f"Processed file {processed_filename} does not have expected row count"
    assert (
        "mean" in processed_df.columns
    ), f"Processed file {processed_filename} does not have 'mean' column"

    # Cleanup - remove created files
    remove_file(test_filename)
    remove_file(processed_filename)


def test_cli_concat():
    """Test the CLI behavior for 'concat' mode."""
    # Create a sample dataframe and save it as a CSV file for testing
    test_df = pd.DataFrame({"A": range(50), "B": range(50, 100)})
    test_filename = "test_data_df.csv"
    test_df.to_csv(test_filename, index=False)

    # Run the script with the 'concat' mode
    subprocess.run(
        ["best_science_ever", "concat", test_filename, test_filename, test_filename],
        check=True,
    )

    # Check if the concatenated file is created correctly
    concatenated_filename = "test_data_df_processed.csv"
    assert os.path.exists(
        concatenated_filename
    ), f"Concatenated file {concatenated_filename} does not exist"
    concatenated_df = pd.read_csv(concatenated_filename)
    assert (
        len(concatenated_df) == 150
    ), f"Concatenated file {concatenated_filename} does not have expected row count"

    # Cleanup - remove created files
    remove_file(test_filename)
    remove_file(concatenated_filename)


def test_cli_invalid_mode():
    """Test the CLI behavior with an invalid mode."""
    result = subprocess.run(
        ["best_science_ever", "invalid_mode", "dummy.csv"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert (
        result.returncode != 0
    ), "Script should exit with a non-zero exit code for invalid mode"
    assert (
        "invalid choice: 'invalid_mode'" in result.stderr.decode()
    ), "Expected error message not found in stderr"


def test_splitting_is_same_as_concatenating():
    """Test that splitting and concatenating a dataframe gives the same result."""
    df = pd.DataFrame(np.random.rand(100, 5))  # Create a random dataframe
    split_dfs = split(df, 10)
    concatenated_df = concat(split_dfs)
    assert len(concatenated_df) == len(
        df
    ), "Splitting and concatenating a dataframe should give the same result"


def test_splitting_same_number_of_rows():
    """Test that splitting a dataframe gives the same number of rows."""
    df = pd.DataFrame(np.random.rand(10, 5))  # Create a random dataframe
    split_dfs = split(df, 10)
    assert (
        len(split_dfs) == 1
    ), "Splitting a dataframe should give the same number of rows"


def test_cli_splitting_same_number_of_rows_diff():
    """Test that splitting a dataframe gives the same number of rows."""
    # Create a sample dataframe and save it as a CSV file for testing
    test_df = pd.DataFrame({"A": range(10), "B": range(10, 20)})
    test_filename = "test_data_df.csv"
    test_df.to_csv(test_filename, index=False)

    # Run the script with the 'split' mode
    subprocess.run(
        ["best_science_ever", "split", test_filename, "--n_rows", "10"],
        check=True,
    )

    # Check if the split files are created correctly
    split_filename = "test_data_df_0_processed.csv"
    assert os.path.exists(split_filename), f"Split file {split_filename} does not exist"
    split_df = pd.read_csv(split_filename)
    assert (
        len(split_df) == 10
    ), f"Split file {split_filename} does not have expected row count"

    result = subprocess.run(["diff", test_filename, split_filename])

    assert (
        result.returncode == 0
    ), "Splitting a dataframe with the same number of rows should give the same result"

    # Cleanup - remove created files
    remove_file(test_filename)
    for i in range(1):
        remove_file(f"test_data_{i}_processed.csv")
