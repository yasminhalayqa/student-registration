# Generated by Django 5.0.4 on 2024-05-18 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_courses_courseschedule_students_studentsregs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='students_enrolled',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='students',
            name='courses',
            field=models.ManyToManyField(through='members.studentsRegs', to='members.courses'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='code',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='courses',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.RemoveField(
            model_name='courses',
            name='prerequisites',
        ),
        migrations.AlterField(
            model_name='courses',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='members.courseschedule'),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='endTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='startTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='students',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='studentsregs',
            name='courseId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='members.courses'),
        ),
        migrations.AlterField(
            model_name='studentsregs',
            name='studentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='members.students'),
        ),
        migrations.AddField(
            model_name='courses',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, to='members.courses'),
        ),
    ]
