# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-28 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0030_word_skip_meaning'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='note',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
