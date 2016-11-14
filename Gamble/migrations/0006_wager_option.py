# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gamble', '0005_auto_20151208_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='wager',
            name='option',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
