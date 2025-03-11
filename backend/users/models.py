from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        HR = 'HR', _('HR')
        SALES = 'SALES', _('Sales')
        MANAGER = 'MANAGER', _('Manager')
        FINANCE = 'FINANCE', _('Finance')
        EMPLOYEE = 'EMPLOYEE', _('Employee')

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.EMPLOYEE
    )
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_hr(self):
        return self.role == self.Roles.HR

    @property
    def is_sales(self):
        return self.role == self.Roles.SALES

    @property
    def is_manager(self):
        return self.role == self.Roles.MANAGER

    @property
    def is_finance(self):
        return self.role == self.Roles.FINANCE

    @property
    def is_employee(self):
        return self.role == self.Roles.EMPLOYEE
