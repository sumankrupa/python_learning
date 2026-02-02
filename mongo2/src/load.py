from sqlalchemy import text

def load(engine,project_df,project_technologies_df):
    

    try:
        with engine.begin() as conn:
            project_df.to_sql("projects2", con=conn, if_exists="append", index=False)
            project_technologies_df.to_sql("project_techs", con=conn, if_exists="append", index=False)
            print('loading done')

    except Exception as e:
        print("LOAD FAILED", repr(e))
        raise
