# Generated by Django 2.0 on 2017-12-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiss', '0005_auto_20171226_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='wins',
            field=models.SmallIntegerField(default=0),
        ),
    ]
