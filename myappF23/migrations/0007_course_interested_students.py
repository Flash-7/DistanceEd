# Generated by Django 4.2.6 on 2023-11-21 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappF23', '0006_alter_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='interested_students',
            field=models.ManyToManyField(blank=True, related_name='interested_students', to='myappF23.student'),
        ),
    ]
