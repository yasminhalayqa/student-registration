from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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
    registration_deadline = models.TimeField(null=True)



class Students(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Courses, through='studentsRegs')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)



class studentsRegs(models.Model):
    studentId = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='registrations')
    courseId = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='registrations')



