# Generated by Django 5.0.2 on 2025-03-10 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('layout', models.JSONField()),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DashboardWidget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('widget_type', models.CharField(choices=[('CHART', 'Chart'), ('TABLE', 'Table'), ('KPI', 'Key Performance Indicator'), ('CUSTOM', 'Custom Widget')], max_length=20)),
                ('data_source', models.JSONField()),
                ('position', models.JSONField()),
                ('size', models.JSONField()),
                ('settings', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['dashboard', 'position'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('report_type', models.CharField(choices=[('EMPLOYEE_PERFORMANCE', 'Employee Performance'), ('PROJECT_PROGRESS', 'Project Progress'), ('LEAVE_ANALYTICS', 'Leave Analytics'), ('TIMESHEET_ANALYTICS', 'Timesheet Analytics'), ('CUSTOM', 'Custom Report')], max_length=50)),
                ('format', models.CharField(choices=[('PDF', 'PDF'), ('EXCEL', 'Excel'), ('CSV', 'CSV'), ('JSON', 'JSON')], max_length=20)),
                ('parameters', models.JSONField(default=dict)),
                ('schedule', models.JSONField(blank=True, default=dict)),
                ('is_scheduled', models.BooleanField(default=False)),
                ('last_generated', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReportExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True)),
                ('result_file', models.FileField(blank=True, null=True, upload_to='report_results/')),
                ('parameters_used', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReportTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('report_type', models.CharField(choices=[('EMPLOYEE_PERFORMANCE', 'Employee Performance'), ('PROJECT_PROGRESS', 'Project Progress'), ('LEAVE_ANALYTICS', 'Leave Analytics'), ('TIMESHEET_ANALYTICS', 'Timesheet Analytics'), ('CUSTOM', 'Custom Report')], max_length=50)),
                ('template_data', models.JSONField()),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
