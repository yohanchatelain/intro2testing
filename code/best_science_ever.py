#!/usr/bin/env


from argparse import ArgumentParser
import pandas as pd
import numpy as np


def split(df, n_rows):
    dfs = []
    start = 0
    while True:
        tmpdf = df.iloc[start:start+n_rows]
        if len(tmpdf) < 1:
            break

        dfs += [tmpdf]
        del tmpdf
        start += n_rows

    return dfs


def concat(dfs):
    for idx, tmpdf in enumerate(dfs):
        if not idx:
            df = tmpdf
        else:
            df = pd.concat(df, tmpdf)
    return df


def process(df):
    df['mean'] = None
    for idx, row in df.iterrows():
        row['mean'] = np.mean(row.values)
    return df


def main():
    parser = ArgumentParser(__file__, description="This tool performs the "
                            "COOLEST science... aka, the following: either "
                            "splits a dataframe, computes some features on one,"
                            " or merges a few equivalent dataframes.")
    parser.add_argument("mode", action="store", default="split",
                        choices=["split", "process", "concat"],
                        help="The function to perform on your dataframe. "
                             "Split: separates the dataframe into multiple "
                             "smaller ones. Process: computes some features of "
                             "the dataframe. Concat: merges dataframes.")
    parser.add_argument("df", action="store", nargs="+",
                        help="Data frame(s) containing a bunch of rows.")

    parser.add_argument("--n_rows", "-n", action="store", type=int, default=10,
                        help="The number of rows per output dataframe. Used by "
                             "\"split\" mode.")

    results = parser.parse_args()

    # Load DF
    tmp_dfs, n_rows = results.df, results.n_rows
    if len(tmp_dfs) == 1:
        df = pd.read_csv(tmp_dfs[0])
    else:
        dfs = [pd.read_csv(tmp_df) for tmp_df in tmp_dfs]

    # Assign the correct functions and apply one
    fn_mapping = {"split": lambda df, n_rows: split(df, n_rows),
                  "process": lambda df, n_rows: process(df),
                  "concat": lambda df, n_rows: concat(df)}
    new_df = fn_mapping[results.mode](df, n_rows)

    # Save the new dataframe
    if isinstance(new_df, list):
        for _idx, ndf in enumerate(new_df):
            ndf.to_csv(tmp_dfs[0].replace('.csv',
                                          '_{0}_processed.csv'.format(_idx)))
    else:
        new_df.to_csv(tmp_dfs[0].replace('.csv','_processed.csv'))


if __name__ == "__main__":
    main()

