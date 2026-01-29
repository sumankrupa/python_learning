

import pandas as pd 

def load_data(dim_df,engine):
    
    dim_df.to_sql(
        'dim_customers_scd2',
        con = engine,
        if_exists = 'append',
        index = False,

    )
    print('loading done')
    return 