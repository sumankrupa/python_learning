import pandas as pd 

def transform(data):
    dummy = [{
        "project_id": "HCL001",
        "project_name": "Cloud Infra Automation",
        "client": {
          "name": "FinTrust Corp",
          "industry": "Banking",
          "location": {
            "city": "New York",
            "country": "USA"
          }
        },
        "technologies": ["AWS", "Terraform", "Python"],
        "status": "In Progress",
        "team": {
          "project_manager": "Amit Sinha",
          "members": [
            {"name": "Riya Mehta", "role": "DevOps Engineer"},
            {"name": "Sagar Patel", "role": "Cloud Architect"}
          ]
        },
        "milestones": [
          {"name": "Setup Infrastructure", "due_date": "2024-06-01"},
          {"name": "Monitoring & Alerts", "due_date": "2024-07-01"}
        ]
      }]


    map = {
        'In Progress' : 'Active',
        'Planned' : 'Pending',
        'Completed' : 'Done'
    }

    projects = []
    project_technologies = []
    project_team_members = []
    project_milestones = []

    for p in dummy:
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


    for p in dummy:
        techs = p.get('technologies')
        for t in techs:

            project_technologies.append({
                
                'tech_name':t,
                'project_id':p.get('project_id')
            })

    for p in dummy:
        members = p.get('team').get('members')
        for member in members:
            project_team_members.append({
                'name':member.get('name'),
                'role':member.get('role'),
                'project_id':p.get('project_id'),
                'manager':p.get('team').get('project_manager')

            })

    for p in dummy:
        milestones = p.get('milestones')
        for m in milestones:
            project_milestones.append({
                'name':m.get('name'),
                'due_date':m.get('due_date'),
                'project_id':p.get('project_id')

            })
    print(projects)
    project_df = pd.DataFrame(projects).drop_duplicates(subset=['project_id'])
    project_technologies_df = pd.DataFrame(project_technologies).drop_duplicates()
    project_team_members_df = pd.DataFrame(project_team_members).drop_duplicates()
    project_milestones_df = pd.DataFrame(project_milestones).drop_duplicates()

    return project_df,project_technologies_df,project_team_members_df,project_milestones_df