from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from .models import Courses
from .forms import StudentRegistrationForm
from .forms import StudentLoginForm
from .models import Students
from .models import studentsRegs
from django.db import models
from django.contrib import messages
from datetime import datetime


def members(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())




def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])
            student.save()
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})




def StudentLogin(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                student = Students.objects.get(email=email)
                if student.check_password(password):
                    request.session['student_id'] = student.id
                    return redirect('search_courses')
            except Students.DoesNotExist:
                form.add_error(None, "Invalid email or password")
    else:
        form = StudentLoginForm()
    return render(request, 'login.html', {'form': form})       

 



def SearchCourse(request):
    search = request.GET.get('search', '')
    if search:
        courses = Courses.objects.filter(
            models.Q(code__icontains=search) |
            models.Q(name__icontains=search) |
            models.Q(instructor__icontains=search)
        )
    else:
        courses = Courses.objects.all()
    
    return render(request, 'search_course.html', {'courses': courses, 'search': search})


def course_detail(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    return render(request, 'course_details.html', {'course': course})



def RegisterCourse(request, course_id):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    
    student =get_object_or_404(Students, id=student_id)
    course = get_object_or_404(Courses, id= course_id)

    registration_deadline = course.registration_deadline  
    days_until_deadline = (registration_deadline - datetime.now()).days

    if 0 < days_until_deadline <= 3:
        messages.warning(request, "Registration deadline for this course is approaching!")

        
    if studentsRegs.objects.filter(studentId=student, courseId=course).exists():
        messages.error(request, "you already register in this course")
        return redirect('course_details', course_id=course_id)
    

    missing_prerequisites = course.prerequisites.exclude(id__in=student.courses.all())
    if missing_prerequisites.exists():
        messages.error(request, 'You do not meet the prerequisites for this course.')
        return redirect('course_details', course_id=course_id)
    

    if course.students_enrolled >= course.capacity:
        messages.error(request, 'this course is full')
        return redirect('course_details', course_id=course_id)
    
    for student_course in student.courses.all():
        if student_course.schedule.days == course.schedule.days and \
           student_course.schedule.startTime < course.schedule.endTime and \
           course.schedule.startTime < student_course.schedule.endTime:
            messages.error(request, 'This course conflicts with your schedule.')
            return redirect('course_details', course_id=course_id)
    

    studentsRegs.objects.create(studentId=student, courseId=course)
    course.students_enrolled += 1
    course.save()
    messages.success(request, 'you have been enrolled in this course')
    return redirect('search_courses')



def ViewSchedule(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    
    student = Students.objects.get(pk=student_id)
    courses = student.courses.all()

    return render(request, 'schedule.html', {'courses': courses})



def GenetateReport(request):
    course_enrollment = Courses.objects.values('name','code', 'students_enrolled')
    return render(request, 'reports.html', {'course_enrollment': course_enrollment})



def CompletedPrerequisiteCourses(request):
    student_id = request.session.get('student_id')

    student = Students.objects.get(pk=student_id)
    enrolled_courses = student.courses.all()

    completed_prerequisite_courses = []

    for course in Courses.objects.all():
        if set(course.prerequisites.all()).issubset(enrolled_courses):
            completed_prerequisite_courses.append(course)

    return render(request, 'completed_prerequisite_courses.html', {'courses': completed_prerequisite_courses})
        


