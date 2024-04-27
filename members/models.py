from django.db import models

# Create your models here.

class Courses(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    prerequisites = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    capacity = models.IntegerField()
    schedule = models.ForeignKey('courseSchedule' , on_delete=models.CASCADE , related_name='schedule')

class courseSchedule (models.Model):
    days = models.CharField(max_length=100)
    startTime = models.DateField()
    endTime = models.DateField()
    roomNo = models.CharField(max_length=100)



class studentsRegs(models.Model):
    studentId = models.ForeignKey('Students', on_delete=models.CASCADE, related_name='studentid')
    courseId = models.ForeignKey('Students', on_delete=models.CASCADE, related_name='courseid')


class Students(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


