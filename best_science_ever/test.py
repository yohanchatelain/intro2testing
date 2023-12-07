import os
import subprocess

import numpy as np
import pandas as pd
from best_science_ever import concat, process, split


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
    test_filename = "test_data.csv"
    test_df.to_csv(test_filename, index=False)

    # Run the script with the 'split' mode
    subprocess.run(
        ["python", "best_science_ever.py", "split", test_filename, "--n_rows", "10"],
        check=True,
    )

    # Check if the split files are created correctly
    for i in range(5):  # Expecting 5 files because 50 rows split into groups of 10
        split_filename = f"test_data_{i}_processed.csv"
        assert os.path.exists(
            split_filename
        ), f"Split file {split_filename} does not exist"
        split_df = pd.read_csv(split_filename)
        assert (
            len(split_df) == 10
        ), f"Split file {split_filename} does not have expected row count"

    # Cleanup - remove created files
    os.remove(test_filename)
    for i in range(5):
        os.remove(f"test_data_{i}_processed.csv")


def test_cli_invalid_mode():
    """Test the CLI behavior with an invalid mode."""
    result = subprocess.run(
        ["python", "best_science_ever.py", "invalid_mode", "dummy.csv"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert (
        result.returncode != 0
    ), "Script should exit with a non-zero exit code for invalid mode"
    assert (
        "invalid choice: 'invalid_mode'" in result.stderr.decode()
    ), "Expected error message not found in stderr"
