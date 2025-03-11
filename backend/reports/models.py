from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Report(models.Model):
    class Type(models.TextChoices):
        EMPLOYEE_PERFORMANCE = 'EMPLOYEE_PERFORMANCE', _('Employee Performance')
        PROJECT_PROGRESS = 'PROJECT_PROGRESS', _('Project Progress')
        LEAVE_ANALYTICS = 'LEAVE_ANALYTICS', _('Leave Analytics')
        TIMESHEET_ANALYTICS = 'TIMESHEET_ANALYTICS', _('Timesheet Analytics')
        CUSTOM = 'CUSTOM', _('Custom Report')

    class Format(models.TextChoices):
        PDF = 'PDF', _('PDF')
        EXCEL = 'EXCEL', _('Excel')
        CSV = 'CSV', _('CSV')
        JSON = 'JSON', _('JSON')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=50, choices=Type.choices)
    format = models.CharField(max_length=20, choices=Format.choices)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_reports'
    )
    parameters = models.JSONField(default=dict)
    schedule = models.JSONField(default=dict, blank=True)
    is_scheduled = models.BooleanField(default=False)
    last_generated = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"

class ReportTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=50, choices=Report.Type.choices)
    template_data = models.JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_templates'
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"

class ReportExecution(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')

    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='executions'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    result_file = models.FileField(
        upload_to='report_results/',
        null=True,
        blank=True
    )
    parameters_used = models.JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_executions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.report.name} - {self.get_status_display()}"

class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    layout = models.JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_dashboards'
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class DashboardWidget(models.Model):
    class Type(models.TextChoices):
        CHART = 'CHART', _('Chart')
        TABLE = 'TABLE', _('Table')
        KPI = 'KPI', _('Key Performance Indicator')
        CUSTOM = 'CUSTOM', _('Custom Widget')

    dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name='widgets'
    )
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=Type.choices)
    data_source = models.JSONField()
    position = models.JSONField()
    size = models.JSONField()
    settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['dashboard', 'position']

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"
