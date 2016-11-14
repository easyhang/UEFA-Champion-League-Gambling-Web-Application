# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gamble', '0006_wager_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
