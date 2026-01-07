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

## Clone and Setup on New Machine

### **1. Clone Repository:**
```bash
git clone https://github.com/mrnoia/csv-inpector.git
cd csv-inspector
```

### **2. Setup Python Environment:**

#### **Option A: Using UV (Recommended)**
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run python app.py
```

#### **Option B: Using pip**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

# Install dependencies
pip install flask pandas werkzeug

# Run the application
python app.py
```

#### **Option C: Using system Python**
```bash
# Install dependencies globally
pip install flask pandas werkzeug

# Run the application
python app.py
```

### **3. Database Setup:**

The SQLite database will be created automatically when you first run the application:
- **Location**: `csv_inspector.db` in the project directory
- **Auto-initialization**: Database and tables are created on first run
- **No manual setup needed**: Just run the app

### **4. Access the Application:**

Open your browser and navigate to:
- **Local**: `http://localhost:5000`
- **Network**: `http://YOUR_IP:5000` (replace with your machine's IP)

### **5. Development Workflow:**

```bash
# Start development server
uv run python app.py

# The server will auto-reload on file changes
# Access at http://localhost:5000

# Check git status
git status

# Add new changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main
```

### **6. Troubleshooting:**

#### **Port already in use:**
```bash
# Kill existing Python processes
pkill -f "python app.py"

# Or use different port
uv run python app.py --port 5001
```

#### **Database issues:**
```bash
# Remove corrupted database
rm csv_inspector.db

# Application will recreate it on next run
```

#### **Dependency issues:**
```bash
# Clear cache and reinstall
uv cache clean
uv sync

# Check Python version
python --version  # Should be 3.12+
```

### **7. Project Structure After Clone:**

```
csv-inspector/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Frontend template
├── pyproject.toml          # Project dependencies
├── README.md              # Project documentation
├── .gitignore             # Git exclusions
├── GIT_SETUP.md           # This setup guide
└── csv_inspector.db       # SQLite database (created automatically)
```

### **8. Environment Variables (Optional):**

Create a `.env` file for configuration:
```bash
# Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database configuration
DATABASE_URL=sqlite:///csv_inspector.db
```

### **9. Production Deployment:**

For production deployment, consider:
- **WSGI Server**: Use Gunicorn or uWSGI
- **Environment Variables**: Set FLASK_ENV=production
- **Database Backup**: Regular database backups
- **Security**: Use HTTPS and secure headers

### **10. Quick Start Commands:**

```bash
# Clone and setup (one command)
git clone https://github.com/mrnoia/csv-inpector.git && cd csv-inspector && uv sync && uv run python app.py

# Or step by step
git clone https://github.com/mrnoia/csv-inpector.git
cd csv-inspector
uv sync
uv run python app.py
```

This setup gets you running quickly on any new machine!

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
