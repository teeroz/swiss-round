# Generated by Django 2.1.7 on 2022-09-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiss', '0011_auto_20180105_1132_squashed_0014_league_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='win_mode',
            field=models.CharField(default='', max_length=32),
        ),
    ]
