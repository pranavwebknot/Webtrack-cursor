from rest_framework import serializers
from .models import Report, ReportTemplate, ReportExecution, Dashboard, DashboardWidget
from users.serializers import UserSerializer

class ReportSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)
    last_execution = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'last_generated')

    def get_last_execution(self, obj):
        last_execution = obj.executions.filter(
            status=ReportExecution.Status.COMPLETED
        ).first()
        if last_execution:
            return {
                'id': last_execution.id,
                'completed_at': last_execution.completed_at,
                'result_file': last_execution.result_file.url if last_execution.result_file else None
            }
        return None

    def create(self, validated_data):
        created_by_id = validated_data.pop('created_by_id')
        validated_data['created_by_id'] = created_by_id
        return super().create(validated_data)

class ReportTemplateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReportTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        created_by_id = validated_data.pop('created_by_id')
        validated_data['created_by_id'] = created_by_id
        return super().create(validated_data)

class ReportExecutionSerializer(serializers.ModelSerializer):
    report_name = serializers.CharField(source='report.name', read_only=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)
    result_file_url = serializers.SerializerMethodField()

    class Meta:
        model = ReportExecution
        fields = '__all__'
        read_only_fields = ('created_at', 'started_at', 'completed_at', 'error_message')

    def get_result_file_url(self, obj):
        return obj.result_file.url if obj.result_file else None

    def create(self, validated_data):
        created_by_id = validated_data.pop('created_by_id')
        validated_data['created_by_id'] = created_by_id
        return super().create(validated_data)

class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DashboardSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)
    widgets = DashboardWidgetSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        created_by_id = validated_data.pop('created_by_id')
        validated_data['created_by_id'] = created_by_id
        return super().create(validated_data)

class DashboardCreateSerializer(serializers.ModelSerializer):
    created_by_id = serializers.IntegerField(write_only=True)
    widgets = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    class Meta:
        model = Dashboard
        fields = ('name', 'description', 'layout', 'is_public', 'created_by_id', 'widgets')

    def create(self, validated_data):
        widgets_data = validated_data.pop('widgets', [])
        created_by_id = validated_data.pop('created_by_id')
        validated_data['created_by_id'] = created_by_id

        dashboard = Dashboard.objects.create(**validated_data)

        for widget_data in widgets_data:
            DashboardWidget.objects.create(dashboard=dashboard, **widget_data)

        return dashboard

class ReportExecutionCreateSerializer(serializers.ModelSerializer):
    report_id = serializers.IntegerField(write_only=True)
    created_by_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReportExecution
        fields = ('report_id', 'parameters_used', 'created_by_id')

    def create(self, validated_data):
        report_id = validated_data.pop('report_id')
        created_by_id = validated_data.pop('created_by_id')
        validated_data['report_id'] = report_id
        validated_data['created_by_id'] = created_by_id
        return super().create(validated_data)
