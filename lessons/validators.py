from rest_framework import serializers


class LessonCustomValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        result = "youtube.com" in str(value).lower()

        if not result:
            message = "The link should lead to youtube.com"
            raise serializers.ValidationError(message)
