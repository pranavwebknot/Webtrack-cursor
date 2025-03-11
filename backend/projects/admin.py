from django.contrib import admin
from .models import Project, Task, ProjectMember, ProjectComment, ProjectDocument

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class ProjectCommentInline(admin.TabularInline):
    model = ProjectComment
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'client', 'project_manager', 'start_date', 'end_date',
        'status', 'budget', 'actual_cost', 'created_at'
    )
    list_filter = ('status', 'client', 'start_date', 'end_date', 'project_manager')
    search_fields = ('name', 'client', 'description')
    readonly_fields = ('created_at', 'updated_at', 'actual_cost')
    inlines = [ProjectMemberInline, TaskInline, ProjectCommentInline, ProjectDocumentInline]
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project_manager')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'project', 'assigned_to', 'status', 'priority',
        'start_date', 'due_date', 'estimated_hours', 'actual_hours'
    )
    list_filter = ('status', 'priority', 'project', 'assigned_to', 'start_date', 'due_date')
    search_fields = ('title', 'description', 'project__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'assigned_to')

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role', 'start_date', 'end_date', 'allocation_percentage')
    list_filter = ('role', 'project', 'user', 'start_date', 'end_date')
    search_fields = ('project__name', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'user')

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'content', 'created_at')
    list_filter = ('project', 'user', 'created_at')
    search_fields = ('content', 'project__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'user')

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'uploaded_by', 'created_at')
    list_filter = ('project', 'uploaded_by', 'created_at')
    search_fields = ('title', 'description', 'project__name', 'uploaded_by__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'uploaded_by')
