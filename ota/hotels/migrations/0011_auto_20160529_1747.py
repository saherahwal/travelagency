# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_auto_20160519_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('familyScore', models.IntegerField()),
                ('adventureScore', models.IntegerField()),
                ('beachSunScore', models.IntegerField()),
                ('casinosScore', models.IntegerField()),
                ('historyCultureScore', models.IntegerField()),
                ('clubbingScore', models.IntegerField()),
                ('romanceScore', models.IntegerField()),
                ('shoppingScore', models.IntegerField()),
                ('skiingScore', models.IntegerField()),
                ('wellnessScore', models.IntegerField()),
                ('hotel', models.ForeignKey(related_name='hotel', to='hotels.Hotel')),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
        migrations.RemoveField(
            model_name='scores',
            name='hotel',
        ),
        migrations.DeleteModel(
            name='Scores',
        ),
    ]
