# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mosquito', '0005_auto_20170313_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='report_date',
            field=models.DateTimeField(),
        ),
    ]
