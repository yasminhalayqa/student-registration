from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('register/', views.register, name='register'),
    path('login/', views.StudentLogin, name='login'),
    path('search/', views.SearchCourse, name='search_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_details'),
      path('', views.course_list, name='course_list'),
    path('add/<int:course_id>/', views.add_course, name='add_course'),
    path('schedule/', views.view_schedule, name='view_schedule'),


]