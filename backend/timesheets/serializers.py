from rest_framework import serializers
from .models import Project, Timesheet, TimesheetEntry
from users.serializers import UserSerializer
from django.utils import timezone

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TimesheetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TimesheetSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    entries = TimesheetEntrySerializer(many=True, read_only=True)
    approved_by = UserSerializer(read_only=True)

    class Meta:
        model = Timesheet
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'total_hours', 'approved_at')

class TimesheetCreateSerializer(serializers.ModelSerializer):
    entries = TimesheetEntrySerializer(many=True)
    project_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Timesheet
        fields = ('project_id', 'week_start_date', 'notes', 'entries')
        read_only_fields = ('employee', 'status', 'total_hours', 'approved_by', 'approved_at')

    def create(self, validated_data):
        entries_data = validated_data.pop('entries')
        validated_data['employee'] = self.context['request'].user
        timesheet = Timesheet.objects.create(**validated_data)
        for entry_data in entries_data:
            TimesheetEntry.objects.create(timesheet=timesheet, **entry_data)
        return timesheet

class TimesheetUpdateSerializer(serializers.ModelSerializer):
    entries = TimesheetEntrySerializer(many=True)

    class Meta:
        model = Timesheet
        fields = ('notes', 'entries')
        read_only_fields = ('employee', 'project', 'week_start_date', 'status', 'total_hours', 'approved_by', 'approved_at')

    def update(self, instance, validated_data):
        entries_data = validated_data.pop('entries')
        instance.entries.all().delete()  # Remove existing entries
        for entry_data in entries_data:
            TimesheetEntry.objects.create(timesheet=instance, **entry_data)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance

class TimesheetApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = ('status',)
        read_only_fields = ('employee', 'project', 'week_start_date', 'notes', 'total_hours', 'approved_by', 'approved_at')

    def update(self, instance, validated_data):
        if instance.status == Timesheet.Status.DRAFT:
            instance.status = Timesheet.Status.SUBMITTED
        elif instance.status == Timesheet.Status.SUBMITTED:
            instance.status = validated_data.get('status')
            if instance.status == Timesheet.Status.APPROVED:
                instance.approved_by = self.context['request'].user
                instance.approved_at = timezone.now()
        instance.save()
        return instance
