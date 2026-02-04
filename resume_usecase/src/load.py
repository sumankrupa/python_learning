

import pandas as pd 

def load_data(engine,df):
    df.to_sql(
        name = 'resume',
        if_exists = 'append',
        con = engine
    )
   
    print('loading done')
    return 