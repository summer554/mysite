# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-12-16 09:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='create_time',
            new_name='created_time',
        ),
    ]
