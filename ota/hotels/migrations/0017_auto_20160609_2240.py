# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0016_auto_20160609_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topinterestlocation',
            name='description',
        ),
        migrations.AddField(
            model_name='topinterestlocation',
            name='full_desc',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topinterestlocation',
            name='short_desc',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
