# admin.py
from django.contrib import admin
from .models import Courses, courseSchedule

class CoursesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor', 'capacity', 'students_enrolled', 'registration_deadline')


class courseScheduleAdmin(admin.ModelAdmin):
    list_display = ('days', 'startTime', 'endTime', 'roomNo')



admin.site.register(Courses, CoursesAdmin)
admin.site.register(courseSchedule, courseScheduleAdmin)
