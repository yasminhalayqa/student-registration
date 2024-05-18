from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('register/', views.register, name='register'),
    path('login/', views.StudentLogin, name='login'),
    path('search/', views.SearchCourse, name='search_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_details'),
    path('add_course/<int:course_id>/', views.RegisterCourse, name='add_course'),
    path('view_schedule/', views.ViewSchedule, name='view_schedule'),



]