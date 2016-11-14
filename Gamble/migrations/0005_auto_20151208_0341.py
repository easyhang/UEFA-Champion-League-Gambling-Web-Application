# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gamble', '0004_user_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='superuser',
            field=models.BooleanField(default=False),
        ),
    ]
