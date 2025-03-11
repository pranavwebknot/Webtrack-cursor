#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create database and sample data
python scripts/setup_db.py

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser --username admin --email admin@example.com --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.get(username='admin').set_password('admin123')"

# Run development server
python manage.py runserver

# Create Django project
django-admin startproject core .

# Create apps
python manage.py startapp users
python manage.py startapp timesheets
python manage.py startapp performance
python manage.py startapp projects
python manage.py startapp leaves
python manage.py startapp reports

# Create necessary directories
mkdir -p media static templates
mkdir -p users/templates/users
mkdir -p timesheets/templates/timesheets
mkdir -p performance/templates/performance
mkdir -p projects/templates/projects
mkdir -p leaves/templates/leaves
mkdir -p reports/templates/reports

# Create .env file
cat > .env << EOL
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/hrm_db
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGIN_WHITELIST=http://localhost:3000
EOL

# Create .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
static/

# Environment variables
.env

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOL

echo "Django project setup completed!"
