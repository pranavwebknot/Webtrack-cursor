from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, PerformanceReviewViewSet, GoalViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'reviews', PerformanceReviewViewSet, basename='review')
router.register(r'goals', GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
]
