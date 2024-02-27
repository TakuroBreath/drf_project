from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lessons.models import Lesson, Course
from users.models import Payment


# Serializers define the API representation.
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    def get_lessons_count(self, course):
        if course.lesson_set.all():
            return course.lesson_set.all().count()
        return 0

    class Meta:
        model = Course
        fields = ['name', 'description', 'lessons', 'lessons_count']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
