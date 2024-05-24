from django.db import models
from django.contrib.auth.models import User

class courseSchedule(models.Model):
    days = models.CharField(max_length=100)
    startTime = models.TimeField()
    endTime = models.TimeField()
    roomNo = models.CharField(max_length=100)


class Courses(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    instructor = models.CharField(max_length=100)
    capacity = models.IntegerField()
    schedule = models.ForeignKey(courseSchedule, on_delete=models.CASCADE, related_name='courses')
    students_enrolled = models.PositiveBigIntegerField(default=0)
    registration_deadline = models.DateTimeField(null=True)




class Students(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Courses, through='studentsRegs')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)



class studentsRegs(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE ,related_name='registrations')
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='registrations') 



