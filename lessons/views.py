from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lessons.models import Course, Lesson, Subscription
from lessons.paginators import CoursePagination, LessonsPagination
from lessons.permissions import IsOwner
from lessons.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve':
            return [IsModerator | IsOwner]
        elif self.action == 'destroy':
            return [IsOwner]
        return super().get_permissions()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsOwner]


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonsPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner ]


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscribeAPIView(APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item, is_active = Subscription.objects.get_or_create(user=user, course=course_item)

        if is_active:
            message = f'Subscribed to {subs_item}'
        else:
            subs_item.delete()
            message = 'Unsubscribed'

        return Response({"message": message})
