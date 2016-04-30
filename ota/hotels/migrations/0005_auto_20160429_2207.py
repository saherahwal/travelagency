# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_auto_20160321_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookNowRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(related_name='book_hotel', to='hotels.Hotel')),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='SearchRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('continent_id', models.SmallIntegerField()),
                ('country_code', models.CharField(max_length=4)),
                ('city', models.CharField(max_length=93)),
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
                ('surpriseme', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
        migrations.AddField(
            model_name='booknowrequest',
            name='searchRequest',
            field=models.ForeignKey(related_name='search_req', to='hotels.SearchRequest'),
            preserve_default=True,
        ),
    ]
