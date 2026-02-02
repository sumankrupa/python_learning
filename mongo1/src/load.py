


def load(engine, project_df,project_technologies_df,project_team_members_df,project_milestones_df):
    with engine.begin() as conn:
        project_df.to_sql(
            name = 'projects',
            con = engine,
            if_exists = 'append',
            index = False
        )
        project_technologies_df.to_sql(
            name = 'projects',
            con = engine,
            if_exists = 'append',
            index = False
        )
        project_team_members_df.to_sql(
            name = 'projects',
            con = engine,
            if_exists = 'append',
            index = False
        )
        project_milestones_df.to_sql(
            name = 'projects',
            con = engine,
            if_exists = 'append',
            index = False
        )
    print('loading done')
    return