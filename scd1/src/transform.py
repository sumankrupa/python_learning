import pandas as pd

def transform(master_df, update_df):
    df1 = master_df.copy()
    df2 = update_df.copy()

    # clean column names (removes accidental spaces)
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    key = "CustomerID"

    # set CustomerID as index
    df1.set_index(key, inplace=True)
    df2.set_index(key, inplace=True)

    # columns to overwrite (SCD Type-1)
    overwrite_cols = ["Email", "Phone"]

    # keep only columns that exist in both dfs
    cols = []
    for c in overwrite_cols:
        if c in df1.columns and c in df2.columns:
            cols.append(c)

    # existing customers
    common_ids = df1.index.intersection(df2.index)

    # overwrite values for existing customers
    df1.loc[common_ids, cols] = df2.loc[common_ids, cols]

    # insert new customers
    new_ids = df2.index.difference(df1.index)
    if len(new_ids) > 0:
        df1 = pd.concat([df1, df2.loc[new_ids]], axis=0)

    df1.reset_index(inplace=True)

    print('transform done')
    return df1
