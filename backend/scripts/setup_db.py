import os
import django
import mysql.connector
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import models
from users.models import User
from projects.models import Project, Task, ProjectMember, ProjectComment, ProjectDocument
from leave.models import LeaveType, LeaveRequest, LeaveBalance, LeavePolicy
from reports.models import Report, ReportTemplate, ReportExecution, Dashboard, DashboardWidget
from timesheet.models import Timesheet, TimesheetEntry
from performance.models import Skill, PerformanceReview, SkillRating, Goal

def create_database():
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''  # Update with your MySQL root password
    )
    cursor = conn.cursor()

    # Create database
    cursor.execute('CREATE DATABASE IF NOT EXISTS webtrack_db')

    # Create user and grant privileges
    cursor.execute('CREATE USER IF NOT EXISTS webtrack_user@localhost IDENTIFIED BY "webtrack_password"')
    cursor.execute('GRANT ALL PRIVILEGES ON webtrack_db.* TO webtrack_user@localhost')
    cursor.execute('FLUSH PRIVILEGES')

    cursor.close()
    conn.close()

def create_sample_data():
    # Create regular users
    users = []
    for i in range(1, 6):
        user = User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password='password123',
            first_name=f'User{i}',
            last_name='Test',
            role='employee'
        )
        users.append(user)
        print(f'Created user: {user.username}')

    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print(f'Created admin user: {admin.username}')

    # Create skills
    skills = [
        Skill.objects.create(name='Python', description='Python programming', category='technical'),
        Skill.objects.create(name='React', description='React development', category='technical'),
        Skill.objects.create(name='Communication', description='Communication skills', category='soft'),
        Skill.objects.create(name='Leadership', description='Leadership abilities', category='soft'),
    ]
    print('Created skills')

    # Create projects
    projects = []
    for i in range(1, 4):
        project = Project.objects.create(
            name=f'Project {i}',
            description=f'Description for Project {i}',
            client=f'Client {i}',
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30),
            status='active',
            budget=10000,
            project_manager=users[0]
        )
        projects.append(project)
        print(f'Created project: {project.name}')

        # Add project members
        for user in users[:3]:
            ProjectMember.objects.create(
                project=project,
                user=user,
                role='developer',
                allocation_percentage=100
            )

        # Create tasks for each project
        for j in range(1, 4):
            task = Task.objects.create(
                project=project,
                title=f'Task {j} for {project.name}',
                description=f'Description for Task {j}',
                assigned_to=random.choice(users),
                status='in_progress',
                priority='medium',
                start_date=datetime.now().date(),
                due_date=datetime.now().date() + timedelta(days=7),
                estimated_hours=8
            )
            print(f'Created task: {task.title}')

    # Create leave types and policies
    leave_types = [
        LeaveType.objects.create(name='Annual Leave', description='Paid annual leave'),
        LeaveType.objects.create(name='Sick Leave', description='Paid sick leave'),
        LeaveType.objects.create(name='Maternity Leave', description='Maternity leave'),
        LeaveType.objects.create(name='Paternity Leave', description='Paternity leave'),
    ]
    print('Created leave types')

    for leave_type in leave_types:
        LeavePolicy.objects.create(
            leave_type=leave_type,
            max_days=20,
            min_days_notice=7,
            requires_approval=True
        )

    # Create leave balances
    for user in users:
        for leave_type in leave_types:
            LeaveBalance.objects.create(
                user=user,
                leave_type=leave_type,
                balance=20
            )

    # Create performance reviews
    for user in users:
        review = PerformanceReview.objects.create(
            employee=user,
            reviewer=users[0],
            review_period='2024-Q1',
            status='draft',
            overall_rating=4.0,
            strengths='Good communication skills',
            areas_for_improvement='Time management',
            goals='Complete project on time',
            comments='Overall good performance'
        )
        print(f'Created performance review for: {user.username}')

        # Add skill ratings
        for skill in skills:
            SkillRating.objects.create(
                review=review,
                skill=skill,
                rating=random.randint(3, 5),
                comments=f'Good {skill.name} skills'
            )

    # Create goals
    for user in users:
        goal = Goal.objects.create(
            employee=user,
            title=f'Goal for {user.username}',
            description=f'Description for goal of {user.username}',
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=90),
            status='in_progress',
            progress=0
        )
        print(f'Created goal for: {user.username}')

if __name__ == '__main__':
    print('Creating database...')
    create_database()

    print('Running migrations...')
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')

    print('Creating sample data...')
    create_sample_data()

    print('Setup completed successfully!')
