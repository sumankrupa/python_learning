import pandas as pd 

def transform(data):
    print("transform input docs:", len(data))

    map = {
        'In Progress' : 'Active',
        'Planned' : 'Pending',
        'Completed' : 'Done'
    }
  
    projects = []
    project_technologies = []
    project_team_members = []
    project_milestones = []

    for p in data:
        projects.append({
        "project_id": p.get('project_id'),
        "project_name": p.get('project_name'),
        "client": p.get('client').get('name'),
        "domain": p.get('client').get('industry'),
        "location": p.get('client').get('location').get('city'),
        "technologies": p.get('technologies'),
        "project_manager": p.get('team').get('project_manager'),
        'status':map.get(p.get('status'))
        })


    for p in data:
        techs = p.get('technologies')
        for t in techs:

            project_technologies.append({
                
                'tech_name':t,
                'project_id':p.get('project_id')
            })
    

    for p in data:
        members = p.get('team').get('members')
        for member in members:
            project_team_members.append({
                'name':member.get('name'),
                'role':member.get('role'),
                'project_id':p.get('project_id'),
                'manager':p.get('team').get('project_manager')

            })
   
    for p in data:
        milestones = p.get('milestones')
        for m in milestones:
            project_milestones.append({
                'name':m.get('name'),
                'due_date':m.get('due_date'),
                'project_id':p.get('project_id')

            })
 
    project_df = pd.DataFrame(projects).drop_duplicates(subset=['project_id'])
    project_technologies_df = pd.DataFrame(project_technologies).drop_duplicates()
    project_team_members_df = pd.DataFrame(project_team_members).drop_duplicates()
    project_milestones_df = pd.DataFrame(project_milestones).drop_duplicates()
    print('transform done')
    return project_df,project_technologies_df,project_team_members_df,project_milestones_df