# Generated by Django 5.0.4 on 2024-05-17 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('prerequisites', models.CharField(max_length=100)),
                ('instructor', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='courseSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(max_length=100)),
                ('startTime', models.DateField()),
                ('endTime', models.DateField()),
                ('roomNo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='studentsRegs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseid', to='members.students')),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentid', to='members.students')),
            ],
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.AddField(
            model_name='courses',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='members.courseschedule'),
        ),
    ]