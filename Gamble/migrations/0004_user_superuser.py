# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gamble', '0003_auto_20151207_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='superuser',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
