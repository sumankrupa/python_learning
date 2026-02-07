from sqlalchemy import text

def load_data(engine, df):
    df.to_sql(
        name = 'my_sf_accounts',
        con = engine,
        if_exists = 'append',
        index = False
    )
    
    print('loading done')
    
    return