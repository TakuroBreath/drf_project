from django.core.management import BaseCommand

from lessons.models import Course
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="test@test.com",
            first_name='test',
            last_name='test',
        )
        user.set_password('test')
        user.save()

        course = Course.objects.create(
            name="Test Course",
            description="Test Course description"
        )
        course.save()

        payment = Payment.objects.create(
            user=User.objects.get(pk='1'),
            paid_course=Course.objects.get(pk='1'),
            amount=13000,
            payment_method="cash",
        )
        payment.save()
