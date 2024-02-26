from django.urls import path
from rest_framework.routers import DefaultRouter

from lessons.apps import LessonsConfig
from lessons.views import *

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='LessonList'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='LessonDetail'),
    path('<int:pk>/update/', LessonUpdateAPIView.as_view(), name='LessonUpdate'),
    path('<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='LessonDelete'),
    path('create/', LessonCreateAPIView.as_view(), name='LessonCreate')
] + router.urls
