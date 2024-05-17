from django.contrib import admin
from .models import Students, Courses, courseSchedule, studentsRegs

admin.site.register(Students)
admin.site.register(Courses)
admin.site.register(courseSchedule)
admin.site.register(studentsRegs)

