from django.contrib import admin
from .models import LeaveType, LeaveRequest, LeaveBalance, LeavePolicy

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_days', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'employee', 'leave_type', 'start_date', 'end_date',
        'days_requested', 'status', 'created_at'
    )
    list_filter = ('status', 'leave_type', 'start_date', 'end_date', 'created_at')
    search_fields = (
        'employee__username', 'employee__first_name', 'employee__last_name',
        'leave_type__name', 'reason'
    )
    readonly_fields = ('created_at', 'updated_at', 'days_requested')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'leave_type', 'approved_by')

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = (
        'employee', 'leave_type', 'year', 'total_days',
        'used_days', 'remaining_days'
    )
    list_filter = ('year', 'leave_type', 'created_at')
    search_fields = (
        'employee__username', 'employee__first_name', 'employee__last_name',
        'leave_type__name'
    )
    readonly_fields = ('created_at', 'updated_at', 'remaining_days')
    ordering = ('-year', 'leave_type')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'leave_type')

@admin.register(LeavePolicy)
class LeavePolicyAdmin(admin.ModelAdmin):
    list_display = (
        'leave_type', 'min_days_notice', 'max_consecutive_days',
        'requires_approval', 'requires_documentation'
    )
    list_filter = ('requires_approval', 'requires_documentation', 'created_at')
    search_fields = ('leave_type__name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('leave_type',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('leave_type')
