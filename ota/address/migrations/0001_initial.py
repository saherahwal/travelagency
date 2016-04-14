# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_name', models.CharField(max_length=50)),
                ('country_code', models.CharField(max_length=2)),
                ('phone_code', models.CharField(default=b'000', max_length=3)),
                ('country_name_ar', models.CharField(default=b'', max_length=50)),
            ],
            options=None,
            bases=None,
            managers=None,
        ),
    ]
