from sqlalchemy import text

def load(engine, project_df, project_technologies_df, project_team_members_df, project_milestones_df):
    print("ENTERED LOAD ✅")
    print("ENGINE:", engine.url)

    try:
        with engine.begin() as conn:
            # quick connectivity test
            conn.execute(text("SELECT 1"))
            print("DB CONNECT OK ✅")

            # IMPORTANT: use conn (not engine)
            project_df.to_sql("projects", con=conn, if_exists="append", index=False)
            project_technologies_df.to_sql("project_technologies", con=conn, if_exists="append", index=False)
            project_team_members_df.to_sql("project_team_members", con=conn, if_exists="append", index=False)
            project_milestones_df.to_sql("project_milestones", con=conn, if_exists="append", index=False)

        print("LOAD DONE ✅")

    except Exception as e:
        print("LOAD FAILED ❌", repr(e))
        raise
