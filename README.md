# Software testing and continuous integration tutorial

Base repo for teaching testing at [BrainHack Montreal 2023](https://brainhackmtl.github.io/global2023/)

## Material

This tutorial is based on Greg Kiar's work [here](https://school.brainhackmtl.org/modules/testing/) BrainHack 2020, which François Paugam extended for BrainHack 2022.

This project extends the original tutorial with the use of `pytest` and GitHub Actions.
The project structure has been reorganized to be used with `pytest`.
The original scripts used by Greg in his video are located in the `best_science_ever/` directory if you want to reproduce the experiments Greg shows in his video.

Video content is available:

[![here](https://img.youtube.com/vi/VibDC49ZAJE/0.jpg)](https://youtu.be/VibDC49ZAJE "Presentation")

### Warning

Greg uses Travis-CI.org to conducte remote tests on his GitHub repo.
Since 2021, Travis-CI.org no longer exists; there is only the commercial Travic-CI.com.
So, instead, we will use GitHub Actions here.
You can follow the video up until 55:23, then follow the instructions below to set up the GitHub Actions workflow.


## Installation

### Requirements

You need `git` and `python>=3.8` installed.

If you want to work in an isolated environment, you can work in the following Docker image

```bash
docker pull python:3.10
docker run -it python:3.10 /bin/bash
```

### Fork the repo

1. Visit the GitHub repository at [https://github.com/yohanchatelain/intro2testing](https://github.com/yohanchatelain/intro2testing).

2. In the top-right corner of the page, you'll find a button labeled "Fork". Click on this button.

3. If prompted, select the account under which you want to fork the repository.

4. Once the forking process is complete, you'll have your copy of the repository under your GitHub account. You can then clone, modify, and push changes to this forked repository.

Remember, after forking the repository, you should clone your fork to your local machine to start working on it. You can do this by using the `git clone` command with the URL of your forked repository. For example:

```bash
git clone https://github.com/[your-username]/intro2testing
```

Replace `[your-username]` with your actual GitHub username. After cloning, you can make changes, commit them, and push them back to your forked repository. When you're ready, you can create a pull request to the original repository to propose incorporating your changes.

### Create a virtual environment

If you don't want to mess up your current Python setup

```bash
# Create a new virtual environment named brainhack-tutorial-ci
python3 -m venv brainhack-tutorial-ci
# Activate the environment
source brainhack-tutorial-ci/bin/activate
```

### Install the package

Have a look at `pyproject.toml`, which configures the project and installs the dependencies.

```bash
pip install .
```

### Run the tests

Run the tests located in `best_science_ever/tests/test_best_science_ever.py`.
Add `-v` to enable verbose mode.

```bash
pytest -v
```

All the tests should pass except the last one, mimicking `Test 2` in `best_science_ever/test.sh`

### Fixing the bug

1. Isolate the failing test

   Being able to replay one test without re-executing the entire suite may be helpful, especially when you have a long test suite to run.
   To do so, you can use the `-k <regexp>` option of `pytest` to select tests matching the regexp.

   <details>
   <summary> Answer </summary>

   ```bash
   pytest -v -k test_cli_splitting_same_number_of_rows_diff
   ```
   </details>

2. Try to understand the issue.
   <details>
   <summary> Answer </summary>

    The output from the `diff` command shows a difference between `test_data.csv` and `test_data_0_processed.csv`. Specifically, the processed file (`test_data_0_processed.csv`) includes an additional, unnamed column at the beginning. This additional column appears to be the index of the DataFrame being saved to the CSV file.

    This issue typically occurs when saving a DataFrame to a CSV file in Pandas without specifying that the index should not be included. By default, pandas' `to_csv` method includes the DataFrame index as the first column in the CSV file.
   </details>

3. Fix the bug.
   <details>
   <summary> Answer </summary>

    To fix this, you can modify the `to_csv` call in your `best_science_ever.py` script to include the argument `index=False`. This will prevent pandas from writing the index to the CSV file. The modified line in the `main()` function should look like this:

    ```python
    ndf.to_csv(tmp_dfs[0].replace(".csv", f"_{_idx}_processed.csv"), index=False)
    ```

    And for the case where `new_df` is not a list:

    ```python
    new_df.to_csv(tmp_dfs[0].replace(".csv", "_processed.csv"), index=False)
    ```

    With this modification, the saved CSV files will not include the DataFrame index, and the structure of the output files should match that of the input file more closely.
   </details>
4. Ensure tests are passing.
   <details>
   <summary> Answer </summary>

    ```bash
    pytest -v
    ============================================================== test session starts ==============================================================
    platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.3.0 -- BrainHackMontreal2023/Tutorial_CI_CD/intro2testing/brainhack-tutorial-ci/bin/python3
    cachedir: .pytest_cache
    rootdir: BrainHackMontreal2023/Tutorial_CI_CD/intro2testing
    collected 10 items
    best_science_ever/tests/test_best_science_ever.py::test_split PASSED                                   [ 10%]
    best_science_ever/tests/test_best_science_ever.py::test_process PASSED                                 [ 20%]
    best_science_ever/tests/test_best_science_ever.py::test_concat PASSED                                  [ 30%]
    best_science_ever/tests/test_best_science_ever.py::test_cli_split PASSED                               [ 40%]
    best_science_ever/tests/test_best_science_ever.py::test_cli_process PASSED                             [ 50%]
    best_science_ever/tests/test_best_science_ever.py::test_cli_concat PASSED                              [ 60%]
    best_science_ever/tests/test_best_science_ever.py::test_cli_invalid_mode PASSED                        [ 70%]
    best_science_ever/tests/test_best_science_ever.py::test_splitting_is_same_as_concatenating PASSED      [ 80%]
    best_science_ever/tests/test_best_science_ever.py::test_splitting_same_number_of_rows PASSED           [ 90%]
    best_science_ever/tests/test_best_science_ever.py::test_cli_splitting_same_number_of_rows PASSED       [100%]

    ============================================================== 10 passed in 1.06s ===============================================================
    ```
   </details>

5. Add, commit and push your changes.
   <details>
   <summary> Answer </summary>

   ```bash
   git add best_science_ever/best_science_ever.py
   git commit -m "Fix failing test test_cli_splitting_same_number_of_rows_diff"
   git push
   ```
   </details>
6. Check GitHub action is passing now.
   <details>
   <summary> Answer </summary>
   Here is the answer.
   </details>
