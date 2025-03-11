from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from django_filters import rest_framework as filters
from .models import Skill, PerformanceReview, SkillRating, Goal
from .serializers import (
    SkillSerializer, PerformanceReviewSerializer, PerformanceReviewCreateSerializer,
    PerformanceReviewUpdateSerializer, GoalSerializer, GoalCreateSerializer
)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class PerformanceReviewFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='review_period_start', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='review_period_end', lookup_expr='lte')
    status = filters.ChoiceFilter(choices=PerformanceReview.Status.choices)

    class Meta:
        model = PerformanceReview
        fields = ['employee', 'reviewer', 'status', 'start_date', 'end_date']

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = PerformanceReviewFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return PerformanceReview.objects.all()
        elif user.is_manager:
            return PerformanceReview.objects.filter(employee__manager=user)
        return PerformanceReview.objects.filter(employee=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PerformanceReviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PerformanceReviewUpdateSerializer
        return PerformanceReviewSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def submit_self_review(self, request, pk=None):
        review = self.get_object()
        if review.status != PerformanceReview.Status.DRAFT:
            return Response(
                {'error': 'Only draft reviews can be submitted for self-review.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        review.status = PerformanceReview.Status.SELF_REVIEW
        review.save()
        return Response(self.get_serializer(review).data)

    @action(detail=True, methods=['post'])
    def submit_manager_review(self, request, pk=None):
        review = self.get_object()
        if review.status != PerformanceReview.Status.SELF_REVIEW:
            return Response(
                {'error': 'Only self-reviewed reviews can be submitted for manager review.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        review.status = PerformanceReview.Status.MANAGER_REVIEW
        review.save()
        return Response(self.get_serializer(review).data)

    @action(detail=True, methods=['post'])
    def complete_review(self, request, pk=None):
        review = self.get_object()
        if review.status != PerformanceReview.Status.MANAGER_REVIEW:
            return Response(
                {'error': 'Only manager-reviewed reviews can be completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        review.status = PerformanceReview.Status.COMPLETED
        review.save()
        return Response(self.get_serializer(review).data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = PerformanceReview.objects.all()
        elif user.is_manager:
            queryset = PerformanceReview.objects.filter(employee__manager=user)
        else:
            queryset = PerformanceReview.objects.filter(employee=user)

        total_reviews = queryset.count()
        completed_reviews = queryset.filter(status=PerformanceReview.Status.COMPLETED).count()
        avg_rating = queryset.filter(
            status=PerformanceReview.Status.COMPLETED
        ).aggregate(avg=Avg('overall_rating'))['avg'] or 0

        return Response({
            'total_reviews': total_reviews,
            'completed_reviews': completed_reviews,
            'average_rating': avg_rating,
        })

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Goal.objects.all()
        elif user.is_manager:
            return Goal.objects.filter(employee__manager=user)
        return Goal.objects.filter(employee=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return GoalCreateSerializer
        return GoalSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        goal = self.get_object()
        progress = request.data.get('progress')

        if progress is None:
            return Response(
                {'error': 'Progress value is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            progress = int(progress)
            if not 0 <= progress <= 100:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Progress must be an integer between 0 and 100.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        goal.progress = progress
        if progress == 100:
            goal.status = Goal.Status.COMPLETED
        elif progress > 0:
            goal.status = Goal.Status.IN_PROGRESS

        goal.save()
        return Response(self.get_serializer(goal).data)
