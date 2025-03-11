from rest_framework import serializers
from .models import Project, Task, ProjectMember, ProjectComment, ProjectDocument
from users.serializers import UserSerializer

class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ProjectCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectComment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ProjectDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = ProjectDocument
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        if assigned_to_id:
            validated_data['assigned_to_id'] = assigned_to_id
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    project_manager = UserSerializer(read_only=True)
    project_manager_id = serializers.IntegerField(write_only=True, required=False)
    members = ProjectMemberSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    comments = ProjectCommentSerializer(many=True, read_only=True)
    documents = ProjectDocumentSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'actual_cost')

    def get_progress(self, obj):
        return obj.calculate_progress()

    def create(self, validated_data):
        project_manager_id = validated_data.pop('project_manager_id', None)
        if project_manager_id:
            validated_data['project_manager_id'] = project_manager_id
        return super().create(validated_data)

class ProjectCreateSerializer(serializers.ModelSerializer):
    project_manager_id = serializers.IntegerField(write_only=True)
    initial_members = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    class Meta:
        model = Project
        fields = (
            'name', 'description', 'client', 'start_date', 'end_date',
            'status', 'budget', 'project_manager_id', 'initial_members'
        )

    def create(self, validated_data):
        initial_members = validated_data.pop('initial_members', [])
        project_manager_id = validated_data.pop('project_manager_id')

        project = Project.objects.create(
            project_manager_id=project_manager_id,
            **validated_data
        )

        for member_data in initial_members:
            ProjectMember.objects.create(project=project, **member_data)

        return project

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name', 'description', 'client', 'start_date', 'end_date',
            'status', 'budget', 'project_manager'
        )
        read_only_fields = ('created_at', 'updated_at', 'actual_cost')

class ProjectMemberCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProjectMember
        fields = ('user_id', 'role', 'start_date', 'end_date', 'allocation_percentage')

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        return ProjectMember.objects.create(user_id=user_id, **validated_data)

class ProjectCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectComment
        fields = ('content',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProjectDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = ('title', 'description', 'file')

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)
