from django.contrib import admin
from .models import Project, Timesheet, TimesheetEntry

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'client', 'start_date', 'end_date')
    search_fields = ('name', 'client', 'description')
    ordering = ('-created_at',)

class TimesheetEntryInline(admin.TabularInline):
    model = TimesheetEntry
    extra = 1
    fields = ('date', 'hours', 'description')

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('employee', 'project', 'week_start_date', 'total_hours', 'status', 'approved_by', 'approved_at')
    list_filter = ('status', 'project', 'employee', 'week_start_date', 'approved_by')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name', 'project__name', 'notes')
    readonly_fields = ('total_hours', 'approved_at')
    inlines = [TimesheetEntryInline]
    ordering = ('-week_start_date',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'project', 'approved_by')
