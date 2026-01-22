def load(final_df, engine):

    final_df.to_sql(
        name= 'SCD_01',
        con = engine,
        if_exists = 'replace',
        index = False
    )
    print('loading done')
    return
