# 1. One-Time Setup (Do this once per machine)
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
# check
git config --global --list


# 2. Starting a New Project (Local → GitHub)
# Create project & initialize git

mkdir project_name
cd project_name
git init
git branch -M main

# Create GitHub repo from terminal (BEST way)
gh repo create project_name --public --source=. --remote=origin --push



#  3. Daily Workflow (MOST USED)

# check status
git status

# add files
git add file.csv
git add .


# commit changes
git commit -m "Clear commit message"

# push to git
git push
# pull latest changes
git pull

# 🔹 4. Checking History & Changes
# View commit history

git log
git log --oneline


# see file differences
git diff

# 🔹 5. Branching (Later, but good to know)
# list branches

git branch
git branch -a

# switch branches

git switch main

# 🔹 6. Working With Remotes (GitHub)

# view remotes
git remote -v

# Add remote manually
git remote add origin https://github.com/username/repo.git

# change remote url
git remote set-url origin https://github.com/username/repo.git

# 🔹 7. GitHub CLI (gh) Essentials
# Login
gh auth login
# check login status
gh auth status
# create repo
gh repo create repo_name --public --source=. --push

# clone a repo
gh repo clone username/repo_name

# 🔹 8. Fixing Common Mistakes

# Forgot to add files
git add .
git commit -m "Add missing files"

# Wrong commit message
git commit --amend -m "Correct message"

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Remove file from git but keep locally
git rm --cached file.csv

# 🔹 9. Ignoring Files (VERY IMPORTANT)
# Create .gitignore
touch .gitignore

