import pandas as pd 

# {
#     "project_id": "HCL001",
#     "project_name": "Cloud Infra Automation",
#     "client": {
#       "name": "FinTrust Corp",
#       "industry": "Banking",
#       "location": {
#         "city": "New York",
#         "country": "USA"
#       }
#     },
#     "technologies": ["AWS", "Terraform", "Python"],
#     "status": "In Progress",
#     "team": {
#       "project_manager": "Amit Sinha",
#       "members": [
#         {"name": "Riya Mehta", "role": "DevOps Engineer"},
#         {"name": "Sagar Patel", "role": "Cloud Architect"}
#       ]
#     },
#     "milestones": [
#       {"name": "Setup Infrastructure", "due_date": "2024-06-01"},
#       {"name": "Monitoring & Alerts", "due_date": "2024-07-01"}
#     ]
#   },

def transform(data):

    map = {
        'In Progress' : 'Active',
        'Planned' : 'Pending',
        'Completed' : 'Done'
    }
  
    projects = []
    technologies = []
    
    for p in data:
        projects.append({
        "project_id": p.get('project_id'),
        "project_name": p.get('project_name'),
        "client": p.get('client').get('name'),
        "domain": p.get('client').get('industry'),
        "location": p.get('client').get('location').get('city'),
        
        "project_manager": p.get('team').get('project_manager'),
        'start_date':pd.to_datetime('2026-01-01'),
        'end_date': pd.to_datetime('2026-01-01'),

        'status':map.get(p.get('status'))
        })


    for p in data:
        techs = p.get('technologies')
        for t in techs:

            technologies.append({
                
                'tech_name':t,
                'project_id':p.get('project_id')
            })

    project_df = pd.DataFrame(projects)
    project_technologies_df = pd.DataFrame(technologies)

    if not project_df.empty:
        project_df = project_df.dropna(subset=["project_id", "project_name"])
        project_df["project_id"] = project_df["project_id"].astype(str).str.strip()
        project_df["project_name"] = project_df["project_name"].astype(str).str.strip()

        # remove duplicates by project_id (keep latest)
        project_df = project_df.drop_duplicates(subset=["project_id"], keep="last")

    if not project_technologies_df.empty:
        project_technologies_df = project_technologies_df.dropna(subset=["project_id", "tech_name"])
        project_technologies_df["project_id"] = project_technologies_df["project_id"].astype(str).str.strip()
        project_technologies_df["tech_name"] = project_technologies_df["tech_name"].astype(str).str.strip()
        project_technologies_df = project_technologies_df.drop_duplicates(subset=["project_id", "tech_name"])
    print('transform done')

    return project_df,project_technologies_df