# Generated by Django 5.0.2 on 2024-02-27 16:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_alter_lesson_course'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_payment', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('payment_method', models.CharField(choices=[('cash', 'Cash Payment'), ('transfer', 'Transfer Payment')], max_length=50, verbose_name='payment_method')),
                ('paid_course', models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.SET_NULL, to='lessons.course')),
                ('paid_lesson', models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.SET_NULL, to='lessons.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
