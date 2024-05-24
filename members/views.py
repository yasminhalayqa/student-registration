from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
# from django.contrib.auth import login as auth_login
from .models import Courses
from .forms import StudentRegistrationForm
from .models import Students
from .models import studentsRegs
from django.db import models
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone



def members(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())




def register(request):
    error = ""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('login')
        else:
            error = "Invalid data"

    form = StudentRegistrationForm()

    return render(request, 'register.html', {"form": form, "error": error})





def StudentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username , password = password)
        
        if user is not None:
            login(request, user)
            return redirect('search_courses')
        
        else: return render(request, 'login.html', {'error':"invalid username or password"})
        
    return render(request, 'login.html')
        

 


@login_required
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




@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    return render(request, 'course_details.html', {'course': course})




@login_required
def RegisterCourse(request, course_id):
    
    user_id = request.user.id
    student =  Students.objects.get(user_id=user_id)
    course =  Courses.objects.get(id=course_id)




    registration_deadline = course.registration_deadline  
    days_until_deadline = (registration_deadline - timezone.now()).days
    if 0 < days_until_deadline <= 3:
        messages.warning(request, "Registration deadline for this course is approaching!")




    if studentsRegs.objects.filter(student=student, course=course).exists():
        messages.error(request, "You are already registered in this course.")
        return redirect('course_details', course_id=course_id)




    missing_prerequisites = course.prerequisites.filter(id__in=student.courses.all())
    if missing_prerequisites.exists():
        messages.error(request, 'You do not meet the prerequisites for this course.')
        return redirect('course_details', course_id=course_id)



    if course.students_enrolled >= course.capacity:
        messages.error(request, 'This course is full.')
        return redirect('course_details', course_id=course_id)



    for student_course in student.courses.all():
        if (student_course.schedule.days == course.schedule.days and
            student_course.schedule.startTime < course.schedule.endTime and
            course.schedule.startTime < student_course.schedule.endTime):
            messages.error(request, 'This course conflicts with your schedule.')
            return redirect('course_details', course_id=course_id)



    studentsRegs.objects.create(student=student, course=course)
    course.students_enrolled += 1
    course.save()



    courses_reg = request.session.get('courses_reg', [])
    courses_reg.append(course_id)
    request.session['courses_reg'] = courses_reg

    messages.success(request, 'You have been enrolled in this course.')
    return redirect('search_courses')





@login_required
def ViewSchedule(request):
    user_id = request.user.id
    
    student = Students.objects.get(user_id=user_id)
    
    student_courses = studentsRegs.objects.filter(student=student)
    
    courses=[]

    for reg in student_courses:
        courses.append(reg.course)
        

    return render(request, 'schedule.html', {'courses': courses})


@login_required
def GenetateReport(request):
    course_enrollment = Courses.objects.values('name','code', 'students_enrolled')
    return render(request, 'reports.html', {'course_enrollment': course_enrollment})


@login_required
def CompletedPrerequisiteCourses(request):
    
    user_id = request.user.id
    
    student = Students.objects.get(user_id=user_id)
    enrolled_courses = student.courses.all()

    completed_prerequisite_courses = []

    for course in Courses.objects.all():
        prerequisites = course.prerequisites.all()
        if all(prerequisite in enrolled_courses for prerequisite in prerequisites):
            completed_prerequisite_courses.append(course)

    return render(request, 'completed_prerequisite_courses.html', {'courses': completed_prerequisite_courses})
        


