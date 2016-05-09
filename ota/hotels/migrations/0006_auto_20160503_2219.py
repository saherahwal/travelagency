# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_auto_20160429_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchrequest',
            name='continent_id',
            field=models.SmallIntegerField(null=True),
            preserve_default=True,
        ),
    ]
