from django.urls import path
from rest_framework.routers import DefaultRouter

from lessons.apps import LessonsConfig
from lessons.views import LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDeleteAPIView, \
    LessonCreateAPIView, CourseViewSet, SubscribeAPIView
from users.views import PaymentListAPIView

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='lesson_delete'),
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),

    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),

    path('subscription/', SubscribeAPIView.as_view(), name='subscribe')
] + router.urls
