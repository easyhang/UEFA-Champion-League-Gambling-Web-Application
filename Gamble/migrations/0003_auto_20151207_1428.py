# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gamble', '0002_auto_20151207_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
