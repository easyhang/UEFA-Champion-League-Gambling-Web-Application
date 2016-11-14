# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('speed', models.FloatField()),
                ('attack', models.FloatField()),
                ('technique', models.FloatField()),
                ('sta', models.FloatField()),
                ('defence', models.FloatField()),
                ('power', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='battleArray',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('array', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='match',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('hostness', models.BooleanField(default=True)),
                ('score', models.IntegerField()),
                ('description', models.TextField(max_length=2000)),
                ('date', models.DateField()),
                ('odd', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='player',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('position', models.CharField(max_length=200)),
                ('height', models.FloatField()),
                ('country', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('teamname', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('coach', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=300)),
                ('username', models.CharField(max_length=200)),
                ('balance', models.FloatField(null=True, blank=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='wager',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('fund', models.FloatField()),
                ('done', models.BooleanField(default=False)),
                ('match', models.ForeignKey(to='Gamble.match')),
                ('users', models.ForeignKey(to='Gamble.user')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='Gamble.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team',
            field=models.ForeignKey(to='Gamble.team'),
        ),
        migrations.AddField(
            model_name='battlearray',
            name='match',
            field=models.ForeignKey(to='Gamble.match'),
        ),
        migrations.AddField(
            model_name='ability',
            name='key',
            field=models.ForeignKey(to='Gamble.player'),
        ),
    ]
