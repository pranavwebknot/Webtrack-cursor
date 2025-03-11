from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_days = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)],
        default=0
    )
    is_paid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        CANCELLED = 'CANCELLED', _('Cancelled')

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leave_requests'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.leave_type.name} ({self.start_date} to {self.end_date})"

    def save(self, *args, **kwargs):
        if not self.days_requested:
            # Calculate days between start and end date (inclusive)
            from datetime import timedelta
            self.days_requested = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)

class LeaveBalance(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    year = models.IntegerField()
    total_days = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)]
    )
    used_days = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)],
        default=0
    )
    remaining_days = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'leave_type', 'year']
        ordering = ['-year', 'leave_type']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.leave_type.name} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.remaining_days:
            self.remaining_days = self.total_days - self.used_days
        super().save(*args, **kwargs)

class LeavePolicy(models.Model):
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='policies'
    )
    min_days_notice = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)],
        default=0
    )
    max_consecutive_days = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        default=30
    )
    requires_approval = models.BooleanField(default=True)
    requires_documentation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Leave Policies'
        ordering = ['leave_type']

    def __str__(self):
        return f"Policy for {self.leave_type.name}"
