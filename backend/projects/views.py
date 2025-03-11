from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django_filters import rest_framework as filters
from .models import Project, Task, ProjectMember, ProjectComment, ProjectDocument
from .serializers import (
    ProjectSerializer, ProjectCreateSerializer, ProjectUpdateSerializer,
    TaskSerializer, ProjectMemberSerializer, ProjectMemberCreateSerializer,
    ProjectCommentSerializer, ProjectCommentCreateSerializer,
    ProjectDocumentSerializer, ProjectDocumentCreateSerializer
)

class ProjectFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='end_date', lookup_expr='lte')
    status = filters.ChoiceFilter(choices=Project.Status.choices)
    client = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['status', 'client', 'start_date', 'end_date', 'project_manager']

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ProjectFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        return Project.objects.filter(
            models.Q(project_manager=user) |
            models.Q(members__user=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectUpdateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectMemberCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upload_document(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectDocumentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.filter(
                models.Q(project_manager=user) |
                models.Q(members__user=user)
            ).distinct()

        total_projects = queryset.count()
        active_projects = queryset.filter(status=Project.Status.IN_PROGRESS).count()
        completed_projects = queryset.filter(status=Project.Status.COMPLETED).count()
        total_budget = queryset.aggregate(total=Sum('budget'))['total'] or 0
        total_cost = queryset.aggregate(total=Sum('actual_cost'))['total'] or 0

        return Response({
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_budget': total_budget,
            'total_cost': total_cost,
        })

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(
            models.Q(project__project_manager=user) |
            models.Q(project__members__user=user) |
            models.Q(assigned_to=user)
        ).distinct()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Task.Status.choices):
            return Response(
                {'error': 'Invalid status.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.status = new_status
        task.save()
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        task = self.get_object()
        actual_hours = request.data.get('actual_hours')

        if actual_hours is None:
            return Response(
                {'error': 'Actual hours are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            actual_hours = float(actual_hours)
            if actual_hours < 0:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Actual hours must be a positive number.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.actual_hours = actual_hours
        task.save()
        return Response(self.get_serializer(task).data)

class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ProjectMember.objects.all()
        return ProjectMember.objects.filter(
            models.Q(project__project_manager=user) |
            models.Q(user=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectMemberCreateSerializer
        return ProjectMemberSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
