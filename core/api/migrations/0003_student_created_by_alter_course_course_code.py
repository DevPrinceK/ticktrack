# Generated by Django 4.2.4 on 2023-08-26 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_course_student_uniquecode_course_students_attendance"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="course_code",
            field=models.CharField(max_length=7),
        ),
    ]
