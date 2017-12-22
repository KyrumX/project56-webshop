# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-18 17:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_delete_uservisits'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVisits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visits', models.IntegerField()),
                ('customerID', models.IntegerField(default=0)),
                ('is_staff', models.BooleanField()),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name_plural': 'User Visits',
            },
        ),
    ]
