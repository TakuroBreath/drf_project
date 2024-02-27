from django.contrib.auth.models import AbstractUser
from django.db import models

from lessons.models import Course, Lesson

NULLABLE = {'blank': 'True', 'null': 'True'}


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='email', unique=True)
    avatar = models.ImageField(verbose_name='avatar', **NULLABLE)
    phone = models.CharField(verbose_name='phone', max_length=30, **NULLABLE)
    country = models.CharField(verbose_name='country', max_length=40, **NULLABLE)
    is_active = models.BooleanField(verbose_name='is_active', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    date_of_payment = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE)
    amount = models.IntegerField(verbose_name='amount')

    payment_method_choices = [
        ("cash", "Cash Payment"),
        ("transfer", "Transfer Payment"),
    ]
    payment_method = models.CharField(max_length=50, choices=payment_method_choices, verbose_name="payment_method")
