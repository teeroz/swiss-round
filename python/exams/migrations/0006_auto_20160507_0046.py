# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-06 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_auto_20160506_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='memory',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exams.Book'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='word',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exams.Book'),
        ),
    ]
