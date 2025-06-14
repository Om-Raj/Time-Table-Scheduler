# Generated by Django 5.1.7 on 2025-04-13 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='section',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='timetable.section'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='timetable_id',
            field=models.CharField(max_length=50),
        ),
    ]
