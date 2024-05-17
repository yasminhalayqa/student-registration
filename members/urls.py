from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('members/', views.members, name='members'),
    path('register/', views.register, name='register'),
    path('login/', views.StudentLogin, name='login'),
    path('search/', views.SearchCourse, name='search_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_details'),
      path('course_list', views.course_list, name='course_list'),
    path('add/<int:course_id>/', views.add_course, name='add_course'),
    path('schedule/', views.view_schedule, name='view_schedule'),
    path('schedule/', views.view_schedule, name='view_schedule'),
     path('report/', views.report_view, name='report_view'),
    path('my_schedule/', views.my_schedule, name='my_schedule'),
    path('course/<int:course_id>/register/', views.register_course, name='register_course'),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),




]