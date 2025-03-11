from rest_framework import serializers
from .models import LeaveType, LeaveRequest, LeaveBalance, LeavePolicy
from users.serializers import UserSerializer
from django.utils import timezone

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class LeavePolicySerializer(serializers.ModelSerializer):
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)

    class Meta:
        model = LeavePolicy
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class LeaveBalanceSerializer(serializers.ModelSerializer):
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = LeaveBalance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.IntegerField(write_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'days_requested', 'status', 'approved_by', 'approval_date')

    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        validated_data['employee_id'] = employee_id
        return super().create(validated_data)

class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    leave_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = LeaveRequest
        fields = (
            'employee_id', 'leave_type_id', 'start_date', 'end_date',
            'reason'
        )

    def validate(self, data):
        # Check if the leave request is within the allowed consecutive days
        leave_type = LeaveType.objects.get(id=data['leave_type_id'])
        policy = LeavePolicy.objects.get(leave_type=leave_type)

        days = (data['end_date'] - data['start_date']).days + 1
        if days > policy.max_consecutive_days:
            raise serializers.ValidationError(
                f"Leave request cannot exceed {policy.max_consecutive_days} consecutive days"
            )

        # Check if the request is made with sufficient notice
        from datetime import date
        days_notice = (data['start_date'] - date.today()).days
        if days_notice < policy.min_days_notice:
            raise serializers.ValidationError(
                f"Leave request must be made at least {policy.min_days_notice} days in advance"
            )

        # Check leave balance
        current_year = date.today().year
        try:
            balance = LeaveBalance.objects.get(
                employee_id=data['employee_id'],
                leave_type_id=data['leave_type_id'],
                year=current_year
            )
            if balance.remaining_days < days:
                raise serializers.ValidationError(
                    f"Insufficient leave balance. Remaining days: {balance.remaining_days}"
                )
        except LeaveBalance.DoesNotExist:
            raise serializers.ValidationError("Leave balance not found for the current year")

        return data

    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        leave_type_id = validated_data.pop('leave_type_id')
        validated_data['employee_id'] = employee_id
        validated_data['leave_type_id'] = leave_type_id
        return super().create(validated_data)

class LeaveRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('status', 'rejection_reason')

    def update(self, instance, validated_data):
        if instance.status != LeaveRequest.Status.PENDING:
            raise serializers.ValidationError("Only pending leave requests can be updated")

        status = validated_data.get('status')
        if status == LeaveRequest.Status.APPROVED:
            # Update leave balance
            current_year = instance.start_date.year
            balance = LeaveBalance.objects.get(
                employee=instance.employee,
                leave_type=instance.leave_type,
                year=current_year
            )
            balance.used_days += instance.days_requested
            balance.remaining_days = balance.total_days - balance.used_days
            balance.save()

            # Update leave request
            instance.status = status
            instance.approved_by = self.context['request'].user
            instance.approval_date = timezone.now()
            instance.save()
        elif status == LeaveRequest.Status.REJECTED:
            instance.status = status
            instance.rejection_reason = validated_data.get('rejection_reason', '')
            instance.save()

        return instance
