from sqlalchemy import text

def load(engine, df):
    df.to_sql(
        name = 'gmail_data',
        con = engine,
        if_exists = 'append',
        index = False
    )
    
    print('loading done')
    
    return