from django.contrib import admin
from .models import Report, ReportTemplate, ReportExecution, Dashboard, DashboardWidget

class DashboardWidgetInline(admin.TabularInline):
    model = DashboardWidget
    extra = 1

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'report_type', 'format', 'created_by',
        'is_scheduled', 'last_generated', 'created_at'
    )
    list_filter = ('report_type', 'format', 'is_scheduled', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at', 'last_generated')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'report_type', 'created_by',
        'is_public', 'created_at'
    )
    list_filter = ('report_type', 'is_public', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    list_display = (
        'report', 'status', 'created_by',
        'started_at', 'completed_at', 'created_at'
    )
    list_filter = ('status', 'report__report_type', 'created_at')
    search_fields = (
        'report__name', 'created_by__username',
        'error_message'
    )
    readonly_fields = ('created_at', 'started_at', 'completed_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('report', 'created_by')

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created_by', 'is_public',
        'created_at'
    )
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DashboardWidgetInline]
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'dashboard', 'widget_type',
        'created_at'
    )
    list_filter = ('widget_type', 'dashboard', 'created_at')
    search_fields = ('name', 'dashboard__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('dashboard', 'position')
