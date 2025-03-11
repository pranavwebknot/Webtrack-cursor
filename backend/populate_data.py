import os
import sys
import django
from datetime import datetime, timedelta, date
from decimal import Decimal
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from projects.models import Project, Task, ProjectMember, ProjectComment, ProjectDocument
from leave.models import LeaveType, LeaveRequest, LeaveBalance, LeavePolicy
from performance.models import PerformanceReview, Goal, Skill, SkillRating
from reports.models import ReportTemplate, Report
from webtrack_notifications.models import Notification
from webtrack_analytics.models import AnalyticsMetric

User = get_user_model()

def create_users():
    # Create admin user if it doesn't exist
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'role': 'ADMIN',
            'department': 'IT',
            'position': 'System Administrator',
            'phone_number': '+1234567890',
            'date_of_birth': date(1990, 1, 1),
            'date_of_joining': date(2020, 1, 1),
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()

    # Create HR user if it doesn't exist
    hr_user, created = User.objects.get_or_create(
        username='hr',
        defaults={
            'email': 'hr@example.com',
            'role': 'HR',
            'department': 'Human Resources',
            'position': 'HR Manager',
            'phone_number': '+1234567891',
            'date_of_birth': date(1991, 1, 1),
            'date_of_joining': date(2020, 1, 1)
        }
    )
    if created:
        hr_user.set_password('hr123')
        hr_user.save()

    # Create manager if it doesn't exist
    manager, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'email': 'manager@example.com',
            'role': 'MANAGER',
            'department': 'Project Management',
            'position': 'Senior Project Manager',
            'phone_number': '+1234567892',
            'date_of_birth': date(1992, 1, 1),
            'date_of_joining': date(2020, 1, 1)
        }
    )
    if created:
        manager.set_password('manager123')
        manager.save()

    # Create sales user if it doesn't exist
    sales_user, created = User.objects.get_or_create(
        username='sales',
        defaults={
            'email': 'sales@example.com',
            'role': 'SALES',
            'department': 'Sales',
            'position': 'Sales Manager',
            'phone_number': '+1234567893',
            'date_of_birth': date(1993, 1, 1),
            'date_of_joining': date(2020, 1, 1)
        }
    )
    if created:
        sales_user.set_password('sales123')
        sales_user.save()

    # Create finance user if it doesn't exist
    finance_user, created = User.objects.get_or_create(
        username='finance',
        defaults={
            'email': 'finance@example.com',
            'role': 'FINANCE',
            'department': 'Finance',
            'position': 'Finance Manager',
            'phone_number': '+1234567894',
            'date_of_birth': date(1994, 1, 1),
            'date_of_joining': date(2020, 1, 1)
        }
    )
    if created:
        finance_user.set_password('finance123')
        finance_user.save()

    # Create regular employees if they don't exist
    employees = []
    for i in range(1, 6):
        employee, created = User.objects.get_or_create(
            username=f'employee{i}',
            defaults={
                'email': f'employee{i}@example.com',
                'role': 'EMPLOYEE',
                'department': ['Engineering', 'Marketing', 'Support', 'Operations', 'Design'][i-1],
                'position': ['Software Engineer', 'Marketing Specialist', 'Support Agent', 'Operations Analyst', 'UI/UX Designer'][i-1],
                'phone_number': f'+12345678{i+90}',
                'date_of_birth': date(1994+i, 1, 1),
                'date_of_joining': date(2020, 1, 1)
            }
        )
        if created:
            employee.set_password('employee123')
            employee.save()
        employees.append(employee)

    return {
        'admin': admin_user,
        'hr': hr_user,
        'manager': manager,
        'sales': sales_user,
        'finance': finance_user,
        'employees': employees
    }

def create_projects(manager, employees):
    # Create projects
    projects = []
    project_names = ['Website Redesign', 'Mobile App Development', 'Customer Portal', 'Data Analytics Platform']

    for i, name in enumerate(project_names):
        project = Project.objects.create(
            name=name,
            description=f'Description for {name} project',
            client=f'Client {i+1}',
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            status=Project.Status.IN_PROGRESS,
            budget=Decimal('100000.00'),
            project_manager=manager
        )
        projects.append(project)
        print(f"Created project: {project}")

        # Create tasks for each project
        task_titles = ['Planning', 'Design', 'Development', 'Testing', 'Deployment']
        for j, title in enumerate(task_titles):
            task = Task.objects.create(
                project=project,
                title=f'{title} for {name}',
                description=f'Description for {title} task',
                assigned_to=employees[j % len(employees)],
                status=Task.Status.IN_PROGRESS,
                priority=Task.Priority.MEDIUM,
                start_date=date(2024, 1, 1),
                due_date=date(2024, 12, 31),
                estimated_hours=Decimal('40.00')
            )
            print(f"Created task: {task}")

        # Add project members
        for employee in employees[:3]:  # Add first 3 employees to each project
            ProjectMember.objects.create(
                project=project,
                user=employee,
                role=ProjectMember.Role.DEVELOPER,
                start_date=date(2024, 1, 1),
                allocation_percentage=100
            )
            print(f"Added project member: {employee.get_full_name()} to {project.name}")

        # Add project comments
        for employee in employees:
            ProjectComment.objects.create(
                project=project,
                user=employee,
                content=f'Comment from {employee.get_full_name()} on {project.name}'
            )
            print(f"Added project comment from {employee.get_full_name()}")

    return projects

def create_leave_data(hr, employees):
    # Create leave types
    leave_types = []
    for name, description, days, is_paid in [
        ('Annual Leave', 'Regular vacation days', 20, True),
        ('Sick Leave', 'Days off due to illness', 10, True),
        ('Personal Leave', 'Personal time off', 5, False),
        ('Maternity Leave', 'Leave for new mothers', 90, True),
        ('Paternity Leave', 'Leave for new fathers', 10, True)
    ]:
        leave_type = LeaveType.objects.create(
            name=name,
            description=description,
            default_days=days,
            is_paid=is_paid
        )
        leave_types.append(leave_type)

    # Create leave policies
    for leave_type in leave_types:
        LeavePolicy.objects.create(
            leave_type=leave_type,
            min_days_notice=7,
            max_consecutive_days=leave_type.default_days,
            requires_approval=True
        )

    # Create leave balances
    current_year = date.today().year
    for employee in employees:
        for leave_type in leave_types:
            LeaveBalance.objects.create(
                employee=employee,
                leave_type=leave_type,
                year=current_year,
                total_days=leave_type.default_days,
                used_days=0,
                remaining_days=leave_type.default_days
            )

    # Create leave requests
    for employee in employees:
        for leave_type in leave_types:
            if leave_type.name in ['Annual Leave', 'Sick Leave']:
                LeaveRequest.objects.create(
                    employee=employee,
                    leave_type=leave_type,
                    start_date=date(2024, 6, 1),
                    end_date=date(2024, 6, 5),
                    days_requested=5,
                    status='PENDING',
                    reason='Regular leave request',
                    approval_date=timezone.now()
                )

    return leave_types

def create_performance_data(hr, manager, employees):
    # Create skills
    skills = []
    for name, category, description in [
        ('Python Programming', 'TECHNICAL', 'Python development skills'),
        ('Project Management', 'LEADERSHIP', 'Project management capabilities'),
        ('Communication', 'COMMUNICATION', 'Verbal and written communication'),
        ('Problem Solving', 'PROBLEM_SOLVING', 'Analytical and problem-solving abilities'),
        ('Team Leadership', 'LEADERSHIP', 'Team management and leadership')
    ]:
        skill = Skill.objects.create(
            name=name,
            category=category,
            description=description
        )
        skills.append(skill)

    # Create performance reviews
    for employee in employees:
        review = PerformanceReview.objects.create(
            employee=employee,
            reviewer=manager,
            review_period_start=date(2024, 1, 1),
            review_period_end=date(2024, 12, 31),
            status='DRAFT',
            overall_rating=Decimal('4.0'),
            strengths='Strong technical skills and teamwork',
            areas_for_improvement='Time management',
            goals='Complete project milestones',
            comments=f'Performance review for {employee.get_full_name()}'
        )

        # Add skill ratings
        for skill in skills:
            SkillRating.objects.create(
                review=review,
                skill=skill,
                rating=Decimal('4.0'),
                comments=f'Good {skill.name} skills'
            )

    # Create goals
    for employee in employees:
        Goal.objects.create(
            employee=employee,
            title=f'Career Development Goal {employee.username}',
            description='Improve technical skills and take on more responsibilities',
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            status='IN_PROGRESS',
            progress=50
        )

    return skills

def create_reports(manager, employees):
    # Create report templates
    templates = []
    for name, report_type in [
        ('Project Status Report', 'PROJECT_PROGRESS'),
        ('Employee Performance Report', 'EMPLOYEE_PERFORMANCE'),
        ('Leave Analytics Report', 'LEAVE_ANALYTICS'),
        ('Timesheet Analytics Report', 'TIMESHEET_ANALYTICS'),
        ('Custom Report Template', 'CUSTOM')
    ]:
        template = ReportTemplate.objects.create(
            name=name,
            description=f'Template for {name}',
            report_type=report_type,
            template_data={
                'sections': [
                    {
                        'title': 'Overview',
                        'type': 'text',
                        'content': f'Overview section for {name}'
                    },
                    {
                        'title': 'Data',
                        'type': 'table',
                        'columns': ['Column 1', 'Column 2', 'Column 3']
                    }
                ],
                'filters': [
                    {
                        'name': 'date_range',
                        'type': 'date_range',
                        'label': 'Date Range'
                    }
                ]
            },
            created_by=manager
        )
        templates.append(template)

    # Create reports
    for template in templates:
        Report.objects.create(
            name=f'Generated {template.name}',
            description=f'Generated report from {template.name}',
            report_type=template.report_type,
            format='PDF',
            created_by=manager,
            parameters={
                'date_range': {
                    'start': '2024-01-01',
                    'end': '2024-12-31'
                }
            },
            schedule={
                'frequency': 'MONTHLY',
                'day_of_month': 1
            },
            is_scheduled=True
        )

    return templates

def create_notifications(manager, employees):
    # Create notifications for employees
    for employee in employees:
        Notification.objects.create(
            recipient=employee,
            title='Welcome to WebTrack',
            message='Welcome to the WebTrack platform. Please complete your profile.',
            notification_type='SYSTEM',
            priority='MEDIUM',
            is_read=False
        )

        # Create project-related notifications
        Notification.objects.create(
            recipient=employee,
            title='New Task Assigned',
            message='You have been assigned a new task in the Website Redesign project.',
            notification_type='PROJECT',
            priority='HIGH',
            is_read=False
        )

        # Create leave-related notifications
        Notification.objects.create(
            recipient=employee,
            title='Leave Request Status',
            message='Your leave request for Annual Leave has been submitted.',
            notification_type='LEAVE',
            priority='MEDIUM',
            is_read=False
        )

        # Create performance-related notifications
        Notification.objects.create(
            recipient=employee,
            title='Performance Review',
            message='Your performance review for Q1 2024 is ready.',
            notification_type='PERFORMANCE',
            priority='HIGH',
            is_read=False
        )

        # Create HR-related notifications
        Notification.objects.create(
            recipient=employee,
            title='HR Update',
            message='Please update your emergency contact information.',
            notification_type='HR',
            priority='LOW',
            is_read=False
        )

def create_analytics_data():
    # Create analytics metrics
    for metric_type in ['USER_ACTIVITY', 'PROJECT_PROGRESS', 'LEAVE_STATS', 'PERFORMANCE', 'HR']:
        AnalyticsMetric.objects.create(
            metric_type=metric_type,
            value=Decimal('75.5'),
            timestamp=timezone.now(),
            metadata={
                'description': f'Sample {metric_type.lower()} metric',
                'unit': 'percentage',
                'target': 80.0
            }
        )

def main():
    print("Starting data population...")

    # Create users
    users = create_users()

    # Create projects and related data
    projects = create_projects(users['manager'], users['employees'])

    # Create leave data
    create_leave_data(users['hr'], users['employees'])

    # Create performance data
    create_performance_data(users['hr'], users['manager'], users['employees'])

    # Create reports
    create_reports(users['manager'], users['employees'])

    # Create notifications
    create_notifications(users['manager'], users['employees'])

    # Create analytics data
    create_analytics_data()

    print("Data population completed!")

if __name__ == '__main__':
    main()
