# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_scores_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_url',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotel',
            name='photo_url',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
    ]
