# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_auto_20160529_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopInterestLocations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('familyInterest', models.BooleanField()),
                ('adventureInterest', models.BooleanField()),
                ('beachSunInterest', models.BooleanField()),
                ('casinosInterest', models.BooleanField()),
                ('historyCultureInterest', models.BooleanField()),
                ('clubbingInterest', models.BooleanField()),
                ('romanceInterest', models.BooleanField()),
                ('shoppingInterest', models.BooleanField()),
                ('skiingInterest', models.BooleanField()),
                ('wellnessInterest', models.BooleanField()),
                ('querystring', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
    ]
