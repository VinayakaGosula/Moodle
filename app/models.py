from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)


class Course(models.Model):
    title = models.CharField(max_length=20, unique=True)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    teachers = models.ManyToManyField(User, related_name="course_teacher")
    students = models.ManyToManyField(User, related_name="course_student")


class Announcements(models.Model):      #mod by vinayaka
    title = models.CharField(null=True, max_length=50)
    desc = models.TextField()
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    course = models.ForeignKey(Course, to_field='title', on_delete=models.CASCADE)
