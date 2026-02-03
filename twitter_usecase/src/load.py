



def load_data(engine, df):
    df.to_sql(
        name='reddits',
        con = engine,
        if_exists = 'append',
        index = False,

    )
    print('loading done')
    return