from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lessons.models import Lesson, Course, Subscription
from lessons.validators import LessonCustomValidator


# Serializers define the API representation.
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LessonCustomValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        if course.lesson_set.all():
            return course.lesson_set.all().count()
        return 0

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ['name', 'description', 'lessons', 'lessons_count']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
