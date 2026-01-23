import pandas as pd

def transform(master_df, update_df):

    master_df.update(update_df)
    return master_df
