from rest_framework import serializers
from .models import Skill, PerformanceReview, SkillRating, Goal
from users.serializers import UserSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillRatingSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = SkillRating
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    skill_ratings = SkillRatingSerializer(many=True, read_only=True)
    overall_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        allow_null=True
    )

    class Meta:
        model = PerformanceReview
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PerformanceReviewCreateSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    reviewer_id = serializers.IntegerField(write_only=True)
    skill_ratings = SkillRatingSerializer(many=True)

    class Meta:
        model = PerformanceReview
        fields = (
            'employee_id', 'reviewer_id', 'review_period_start', 'review_period_end',
            'strengths', 'areas_for_improvement', 'goals', 'comments', 'skill_ratings'
        )

    def create(self, validated_data):
        skill_ratings_data = validated_data.pop('skill_ratings')
        employee_id = validated_data.pop('employee_id')
        reviewer_id = validated_data.pop('reviewer_id')

        review = PerformanceReview.objects.create(
            employee_id=employee_id,
            reviewer_id=reviewer_id,
            **validated_data
        )

        for rating_data in skill_ratings_data:
            SkillRating.objects.create(review=review, **rating_data)

        return review

class PerformanceReviewUpdateSerializer(serializers.ModelSerializer):
    skill_ratings = SkillRatingSerializer(many=True)

    class Meta:
        model = PerformanceReview
        fields = (
            'strengths', 'areas_for_improvement', 'goals', 'comments',
            'overall_rating', 'status', 'skill_ratings'
        )
        read_only_fields = ('employee', 'reviewer', 'review_period_start', 'review_period_end')

    def update(self, instance, validated_data):
        skill_ratings_data = validated_data.pop('skill_ratings')
        instance.skill_ratings.all().delete()

        for rating_data in skill_ratings_data:
            SkillRating.objects.create(review=instance, **rating_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class GoalSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class GoalCreateSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Goal
        fields = ('employee_id', 'title', 'description', 'start_date', 'end_date')

    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        return Goal.objects.create(employee_id=employee_id, **validated_data)
