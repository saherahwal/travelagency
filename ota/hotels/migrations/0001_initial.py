# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hotel_booking_id', models.IntegerField()),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=500)),
                ('state_zip', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=93)),
                ('country_cc1', models.CharField(max_length=4)),
                ('ufi', models.IntegerField()),
                ('hotel_class', models.FloatField()),
                ('currency_code', models.CharField(max_length=3)),
                ('minrate', models.DecimalField(null=True, max_digits=13, decimal_places=3, blank=True)),
                ('maxrate', models.DecimalField(null=True, max_digits=13, decimal_places=3, blank=True)),
                ('preferred', models.NullBooleanField()),
                ('nr_rooms', models.SmallIntegerField()),
                ('longitude', models.DecimalField(max_digits=18, decimal_places=15)),
                ('latitude', models.DecimalField(max_digits=18, decimal_places=15)),
                ('public_ranking', models.SmallIntegerField()),
                ('hotel_url', models.CharField(max_length=150)),
                ('photo_url', models.CharField(max_length=150)),
                ('desc_en', models.TextField(blank=True)),
                ('desc_fr', models.TextField(blank=True)),
                ('desc_es', models.TextField(blank=True)),
                ('desc_de', models.TextField(blank=True)),
                ('desc_nl', models.TextField(blank=True)),
                ('desc_it', models.TextField(blank=True)),
                ('desc_pt', models.TextField(blank=True)),
                ('desc_ja', models.TextField(blank=True)),
                ('desc_zh', models.TextField(blank=True)),
                ('desc_pl', models.TextField(blank=True)),
                ('desc_ru', models.TextField(blank=True)),
                ('desc_sv', models.TextField(blank=True)),
                ('desc_ar', models.TextField(blank=True)),
                ('desc_el', models.TextField(blank=True)),
                ('desc_no', models.TextField(blank=True)),
                ('city_unique', models.CharField(max_length=100)),
                ('city_preferred', models.CharField(max_length=100)),
                ('continent_id', models.SmallIntegerField()),
                ('review_score', models.SmallIntegerField()),
                ('review_nr', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='Scores',
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
    ]
