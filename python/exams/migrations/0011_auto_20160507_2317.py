# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-07 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0010_auto_20160507_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='aware_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='forgot_cnt',
            field=models.IntegerField(default=0),
        ),
    ]
