# Generated by Django 5.0.4 on 2024-05-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_rename_courseid_studentsregs_course_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='deadline',
        ),
        migrations.AlterField(
            model_name='courses',
            name='registration_deadline',
            field=models.DateTimeField(null=True),
        ),
    ]
