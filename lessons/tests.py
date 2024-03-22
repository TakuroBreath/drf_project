from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from lessons.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        self.user.set_password("test")
        self.user.save()

        self.course = Course.objects.create(
            name="Test_course",
            description="Test_course",
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='Test_lesson',
            description='Test_lesson',
            video_url="https://www.youtube.com/watch",
            owner=self.user,
            course=self.course
        )

        self.client.force_authenticate(user=self.user)

    def test_list_lessons(self):
        response = self.client.get(
            reverse('lessons:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.id,
                        'name': self.lesson.name,
                        'preview': None,
                        'description': self.lesson.description,
                        'video_url': self.lesson.video_url,
                        'course': self.lesson.course_id,
                        'owner': self.user.id
                    }
                ]
            }
        )

    def test_create_lesson(self):
        data = {
            "name": "test_lesson2",
            "description": "test_lesson2",
            "video_url": "https://www.youtube.com/watch",
            "course": 1
        }

        response = self.client.post(
            reverse('lessons:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json()['name'],
            data['name']
        )

    def test_update_course(self):
        course = Course.objects.create(
            name='Test_course1212',
            description='Test_lesson',
        )

        response = self.client.patch(
            f'/courses/{course.id}/',
            {'description': 'Changed'}
        )

        print(response)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            name='Test_lesson',
            description='Test_lesson',
            video_url="https://www.youtube.com/watch",
            owner=self.user,
            course=self.course
        )

        response = self.client.delete(
            f'/{lesson.id}/delete/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        self.user.set_password("test")
        self.user.save()

        self.course = Course.objects.create(
            name="Test_course",
            description="Test_course",
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        response = self.client.post(
            reverse('lessons:subscribe'),
            data=data
        )
        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'message': 'Subscribed to Sub on Test_course, U: test@test.com'}
        )
