from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import studentsRegs, Courses
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now, timedelta

@receiver(post_save, sender=studentsRegs)
def send_registration_email(sender, instance, **kwargs):
    course = instance.courseId
    student = instance.studentId
    send_mail(
        'Course Registration Successful',
        f'You have successfully registered for {course.name}.',
        settings.DEFAULT_FROM_EMAIL,
        [student.email],
    )

# Function to send reminders for deadlines
def send_deadline_reminders():
    upcoming_courses = Courses.objects.filter(
        schedule__startTime__lte=now() + timedelta(days=7),
        schedule__startTime__gte=now()
    )
    for course in upcoming_courses:
        registrations = course.courseid.all()
        for registration in registrations:
            send_mail(
                'Upcoming Course Deadline Reminder',
                f'This is a reminder for the upcoming course {course.name} which starts on {course.schedule.startTime}.',
                settings.DEFAULT_FROM_EMAIL,
                [registration.studentId.email],
            )
