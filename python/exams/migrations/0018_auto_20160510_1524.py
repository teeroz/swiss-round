# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0017_auto_20160508_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='antonym',
            field=models.ManyToManyField(related_name='_word_antonym_+', to='exams.Word'),
        ),
        migrations.AddField(
            model_name='word',
            name='related',
            field=models.ManyToManyField(related_name='_word_related_+', to='exams.Word'),
        ),
        migrations.AddField(
            model_name='word',
            name='synonym',
            field=models.ManyToManyField(related_name='_word_synonym_+', to='exams.Word'),
        ),
    ]
