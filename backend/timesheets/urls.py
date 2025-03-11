from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TimesheetViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'timesheets', TimesheetViewSet, basename='timesheet')

urlpatterns = [
    path('', include(router.urls)),
]
