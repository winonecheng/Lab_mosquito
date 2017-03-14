# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mosquito', '0007_auto_20170313_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='temperature',
            field=models.FloatField(default=0),
        ),
    ]