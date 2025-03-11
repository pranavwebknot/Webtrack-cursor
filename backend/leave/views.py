from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django_filters import rest_framework as filters
from django.utils import timezone
from .models import LeaveType, LeaveRequest, LeaveBalance, LeavePolicy
from .serializers import (
    LeaveTypeSerializer, LeaveRequestSerializer, LeaveRequestCreateSerializer,
    LeaveRequestUpdateSerializer, LeaveBalanceSerializer, LeavePolicySerializer
)

class LeaveRequestFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='end_date', lookup_expr='lte')
    status = filters.ChoiceFilter(choices=LeaveRequest.Status.choices)
    leave_type = filters.NumberFilter(field_name='leave_type_id')

    class Meta:
        model = LeaveRequest
        fields = ['status', 'leave_type', 'start_date', 'end_date', 'employee']

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class LeavePolicyViewSet(viewsets.ModelViewSet):
    queryset = LeavePolicy.objects.all()
    serializer_class = LeavePolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class LeaveBalanceViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return LeaveBalance.objects.all()
        return LeaveBalance.objects.filter(employee=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = LeaveBalance.objects.all()
        else:
            queryset = LeaveBalance.objects.filter(employee=user)

        current_year = timezone.now().year
        summary = queryset.filter(year=current_year).aggregate(
            total_days=Sum('total_days'),
            used_days=Sum('used_days'),
            remaining_days=Sum('remaining_days')
        )

        return Response({
            'year': current_year,
            'total_days': summary['total_days'] or 0,
            'used_days': summary['used_days'] or 0,
            'remaining_days': summary['remaining_days'] or 0
        })

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = LeaveRequestFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(
            models.Q(employee=user) |
            models.Q(employee__manager=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'create':
            return LeaveRequestCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LeaveRequestUpdateSerializer
        return LeaveRequestSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave_request = self.get_object()
        serializer = LeaveRequestUpdateSerializer(
            leave_request,
            data={'status': LeaveRequest.Status.APPROVED},
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave_request = self.get_object()
        serializer = LeaveRequestUpdateSerializer(
            leave_request,
            data={
                'status': LeaveRequest.Status.REJECTED,
                'rejection_reason': request.data.get('rejection_reason', '')
            },
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = request.user
        if user.is_admin:
            queryset = LeaveRequest.objects.all()
        else:
            queryset = LeaveRequest.objects.filter(
                models.Q(employee=user) |
                models.Q(employee__manager=user)
            ).distinct()

        current_year = timezone.now().year
        summary = queryset.filter(
            start_date__year=current_year
        ).values('status').annotate(
            count=Count('id')
        )

        return Response({
            'year': current_year,
            'status_summary': {
                item['status']: item['count']
                for item in summary
            }
        })
