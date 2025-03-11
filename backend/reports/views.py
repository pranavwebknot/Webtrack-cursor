from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from django_filters import rest_framework as filters
from .models import Report, ReportTemplate, ReportExecution, Dashboard, DashboardWidget
from .serializers import (
    ReportSerializer, ReportTemplateSerializer, ReportExecutionSerializer,
    DashboardSerializer, DashboardCreateSerializer, ReportExecutionCreateSerializer
)

class ReportFilter(filters.FilterSet):
    report_type = filters.ChoiceFilter(choices=Report.Type.choices)
    format = filters.ChoiceFilter(choices=Report.Format.choices)
    created_by = filters.NumberFilter(field_name='created_by_id')
    is_scheduled = filters.BooleanFilter()

    class Meta:
        model = Report
        fields = ['report_type', 'format', 'created_by', 'is_scheduled']

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ReportFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Report.objects.all()
        return Report.objects.filter(created_by=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        report = self.get_object()
        serializer = ReportExecutionCreateSerializer(data=request.data)
        if serializer.is_valid():
            execution = serializer.save(
                report=report,
                created_by=request.user
            )
            # Here you would typically trigger an async task to generate the report
            # For now, we'll just return the execution details
            return Response(
                ReportExecutionSerializer(execution).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = Report.objects.all()
        else:
            queryset = Report.objects.filter(created_by=user)

        summary = queryset.values('report_type').annotate(
            count=Count('id'),
            scheduled_count=Count('id', filter=models.Q(is_scheduled=True))
        )

        return Response({
            'report_types': {
                item['report_type']: {
                    'total': item['count'],
                    'scheduled': item['scheduled_count']
                }
                for item in summary
            }
        })

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ReportTemplate.objects.all()
        return ReportTemplate.objects.filter(
            models.Q(created_by=user) |
            models.Q(is_public=True)
        )

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ReportExecutionViewSet(viewsets.ModelViewSet):
    queryset = ReportExecution.objects.all()
    serializer_class = ReportExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ReportExecution.objects.all()
        return ReportExecution.objects.filter(created_by=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Dashboard.objects.all()
        return Dashboard.objects.filter(
            models.Q(created_by=user) |
            models.Q(is_public=True)
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return DashboardCreateSerializer
        return DashboardSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def add_widget(self, request, pk=None):
        dashboard = self.get_object()
        serializer = DashboardWidgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dashboard=dashboard)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_layout(self, request, pk=None):
        dashboard = self.get_object()
        layout = request.data.get('layout')
        if not layout:
            return Response(
                {'error': 'Layout data is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        dashboard.layout = layout
        dashboard.save()
        return Response(DashboardSerializer(dashboard).data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = Dashboard.objects.all()
        else:
            queryset = Dashboard.objects.filter(
                models.Q(created_by=user) |
                models.Q(is_public=True)
            )

        summary = queryset.aggregate(
            total_dashboards=Count('id'),
            public_dashboards=Count('id', filter=models.Q(is_public=True)),
            total_widgets=Count('widgets')
        )

        return Response(summary)
