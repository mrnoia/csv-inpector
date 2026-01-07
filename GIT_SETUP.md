# Git Setup Guide

## Initialize Git Repository

1. **Initialize Git repository:**
```bash
git init
```

2. **Add all files to Git:**
```bash
git add .
```

3. **Create initial commit:**
```bash
git commit -m "Initial commit: CSV Inspector with SQLite database"
```

## Create GitHub Repository

1. **Go to GitHub.com** and click "New repository"
2. **Repository name**: `csv-inspector` (or your preferred name)
3. **Description**: "Flask web application for CSV file inspection with SQLite database"
4. **Visibility**: Choose Public or Private
5. **Initialize**: Choose "Add a README file" (we already have one)
6. **Click "Create repository"**

## Push to GitHub

1. **Add remote origin:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/csv-inspector.git
```
Replace `YOUR_USERNAME` with your actual GitHub username.

2. **Push to GitHub:**
```bash
git branch -M main
git push -u origin main
```

## Project Structure for Git

```
csv-inspector/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Main HTML template
├── pyproject.toml          # Project dependencies
├── README.md              # Project documentation
├── csv_inspector.db      # SQLite database (will be created)
└── .gitignore            # Git ignore file
```

## Recommended .gitignore

Create a `.gitignore` file to exclude unnecessary files:

```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## Git Commands Reference

### **Basic Workflow:**
```bash
# Check status
git status

# Add specific files
git add app.py templates/index.html

# Commit changes
git commit -m "Add feature: Save/load functionality"

# Push changes
git push

# Pull latest changes
git pull

# View commit history
git log --oneline
```

### **Branch Management:**
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branches
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

## GitHub Features to Use

- **Issues**: Track bugs and feature requests
- **Projects**: Organize work with project boards
- **Actions**: Automate testing and deployment
- **Wiki**: Document additional information
- **Releases**: Tag and publish versions

## Next Steps

1. **Set up Git**: Initialize and commit locally
2. **Create GitHub repo**: Set up remote repository
3. **Push initial code**: Get your project on GitHub
4. **Regular commits**: Commit and push as you develop
5. **Use branches**: For new features without affecting main

## Security Notes

- **Don't commit sensitive data**: API keys, passwords
- **Use .gitignore**: Exclude database files with real data
- **Review commits**: Check what you're pushing before pushing

This will get your CSV Inspector project properly version-controlled on GitHub!
