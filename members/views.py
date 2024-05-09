from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .models import Courses
from django.shortcuts import render, redirect
from .models import Course, StudentSchedule


def members(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def StudentLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username , password = password)
            if user is not None : 
                auth_login(request, user)
                # return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})        


def SearchCourse (request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        courses = Courses.objects.filter(code__icontains=search) | \
                  Courses.objects.filter(name__icontains=search) | \
                  Courses.objects.filter(instructor__icontains=search)
        return render(request , 'search_course.html', {'courses' : courses, 'search': search})
    else:
        return render(request, 'search_course.html') 
    


def course_detail(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    return render(request, 'course_details.html', {'course': course})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_registration/course_list.html', {'courses': courses})

def add_course(request, course_id):
    course = Course.objects.get(id=course_id)
    # Add your logic here to check prerequisites and schedule clashes
    schedule = StudentSchedule.objects.create(student_name="John Doe")
    schedule.courses.add(course)
    return redirect('course_list')

def view_schedule(request):
    schedule = StudentSchedule.objects.filter(student_name="John Doe").first()
    return render(request, 'course_registration/schedule.html', {'schedule': schedule})