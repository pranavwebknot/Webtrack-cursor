from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, ProjectMemberViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'members', ProjectMemberViewSet, basename='project-member')

urlpatterns = [
    path('', include(router.urls)),
]
