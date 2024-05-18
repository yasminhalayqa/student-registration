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

    if studentsRegs.objects.filter(studentId=student, courseId=course).exists():
        messages.error(request, "you already register in this course")
        return redirect('search_courses')
    

    missing_prerequisites = course.prerequisites.exclude(id__in=student.courses.all())
    if missing_prerequisites.exists():
        messages.error(request, 'You do not meet the prerequisites for this course.')
        return redirect('course_detail', course_id=course_id)
    

    if course.students_enrolled >= course.capacity:
        messages.error(request, 'this course is full')
        return redirect('search_courses')
    
    for student_course in student.courses.all():
        if student_course.schedule == course.schedule:
            messages.error(request, 'this course conflict with your schedule')
            return redirect('search_courses')
    

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