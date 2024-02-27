from django.db import models

NULLABLE = {'blank': 'True', 'null': 'True'}


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Course Name')
    preview = models.ImageField(verbose_name='Course Preview', **NULLABLE)
    description = models.TextField(verbose_name='Course Description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Lesson Name')
    description = models.TextField(verbose_name='Lesson Description')
    preview = models.ImageField(verbose_name='Lesson Preview', **NULLABLE)
    video_url = models.URLField(verbose_name='Video URL')

    course = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE)
