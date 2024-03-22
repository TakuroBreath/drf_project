from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail

from drf_project import settings
from lessons.models import Subscription
from users.models import User


@shared_task
def update_message(course_pk):
    course_subs = Subscription.objects.filter(course_id=course_pk)
    recipient_email = []
    for sub in course_subs:

        if sub.is_active:
            recipient_email.append(sub.user.email)

        send_mail(
            subject="Course Updated!",
            message=f'Course "{sub.course.name}"  ',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_email,
            fail_silently=False
        )


@shared_task
def deactivate_user():
    thirty_days = datetime.now() - timedelta(days=30)

    users = User.objects.filter(
        last_login__lt=thirty_days,
        is_staff=False,
        is_superuser=False
    )

    for user in users:
        users.update(is_active=False)
