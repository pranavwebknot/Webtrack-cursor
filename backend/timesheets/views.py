from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from django_filters import rest_framework as filters
from .models import Project, Timesheet, TimesheetEntry
from .serializers import (
    ProjectSerializer, TimesheetSerializer, TimesheetCreateSerializer,
    TimesheetUpdateSerializer, TimesheetApprovalSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class TimesheetFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='week_start_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='week_start_date', lookup_expr='lte')
    project = filters.NumberFilter(field_name='project_id')
    status = filters.ChoiceFilter(choices=Timesheet.Status.choices)

    class Meta:
        model = Timesheet
        fields = ['employee', 'project', 'status', 'start_date', 'end_date']

class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TimesheetFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Timesheet.objects.all()
        elif user.is_manager:
            return Timesheet.objects.filter(employee__manager=user)
        return Timesheet.objects.filter(employee=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TimesheetCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TimesheetUpdateSerializer
        elif self.action == 'approve':
            return TimesheetApprovalSerializer
        return TimesheetSerializer

    def get_permissions(self):
        if self.action in ['approve']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        timesheet = self.get_object()
        serializer = self.get_serializer(timesheet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = Timesheet.objects.all()
        elif user.is_manager:
            queryset = Timesheet.objects.filter(employee__manager=user)
        else:
            queryset = Timesheet.objects.filter(employee=user)

        total_hours = queryset.aggregate(total=Sum('total_hours'))['total'] or 0
        approved_hours = queryset.filter(status=Timesheet.Status.APPROVED).aggregate(total=Sum('total_hours'))['total'] or 0
        pending_hours = queryset.filter(status=Timesheet.Status.SUBMITTED).aggregate(total=Sum('total_hours'))['total'] or 0
        rejected_hours = queryset.filter(status=Timesheet.Status.REJECTED).aggregate(total=Sum('total_hours'))['total'] or 0

        return Response({
            'total_hours': total_hours,
            'approved_hours': approved_hours,
            'pending_hours': pending_hours,
            'rejected_hours': rejected_hours,
        })

    @action(detail=False, methods=['get'])
    def current_week(self, request):
        today = timezone.now().date()
        week_start = today - timezone.timedelta(days=today.weekday())
        timesheet = self.get_queryset().filter(
            employee=request.user,
            week_start_date=week_start
        ).first()

        if timesheet:
            serializer = self.get_serializer(timesheet)
            return Response(serializer.data)
        return Response(None)
