# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gamble', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='hostness',
        ),
        migrations.RemoveField(
            model_name='match',
            name='odd',
        ),
        migrations.RemoveField(
            model_name='match',
            name='score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team',
        ),
        migrations.AddField(
            model_name='match',
            name='guestteam',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='hostteam',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='odd_even',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='odd_lose',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='odd_win',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='score_guest',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='score_host',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='description',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]
