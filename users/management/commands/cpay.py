from django.core.management import BaseCommand

from lessons.models import Course
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment = Payment.objects.create(
            user=User.objects.get(pk='1'),
            paid_course=Course.objects.get(pk='1'),
            amount=13000,
            payment_method="cash",
        )
        payment.save()
