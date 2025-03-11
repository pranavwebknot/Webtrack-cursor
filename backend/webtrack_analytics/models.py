from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AnalyticsMetric(models.Model):
    class MetricType(models.TextChoices):
        USER_ACTIVITY = 'USER_ACTIVITY', _('User Activity')
        PROJECT_PROGRESS = 'PROJECT_PROGRESS', _('Project Progress')
        LEAVE_STATS = 'LEAVE_STATS', _('Leave Statistics')
        PERFORMANCE = 'PERFORMANCE', _('Performance Metrics')
        HR = 'HR', _('HR Analytics')

    metric_type = models.CharField(max_length=20, choices=MetricType.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.value} ({self.timestamp})"
