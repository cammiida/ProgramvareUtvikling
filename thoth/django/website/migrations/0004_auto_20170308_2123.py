# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_course_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='name',
        ),
        migrations.AddField(
            model_name='lecture',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
