from django.contrib import admin
from .models import Skill, PerformanceReview, SkillRating, Goal

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('category', 'name')

class SkillRatingInline(admin.TabularInline):
    model = SkillRating
    extra = 1

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        'employee', 'reviewer', 'review_period_start', 'review_period_end',
        'status', 'overall_rating', 'created_at'
    )
    list_filter = ('status', 'review_period_start', 'review_period_end', 'employee', 'reviewer')
    search_fields = (
        'employee__username', 'employee__first_name', 'employee__last_name',
        'reviewer__username', 'reviewer__first_name', 'reviewer__last_name',
        'strengths', 'areas_for_improvement', 'goals', 'comments'
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SkillRatingInline]
    ordering = ('-review_period_end',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'reviewer')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'start_date', 'end_date', 'status', 'progress', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'employee')
    search_fields = (
        'employee__username', 'employee__first_name', 'employee__last_name',
        'title', 'description'
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-end_date',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee')
