# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-05 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='code',
            field=models.CharField(max_length=200, verbose_name='验证码'),
        ),
    ]
