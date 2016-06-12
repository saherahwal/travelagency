# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0018_auto_20160611_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topinterestlocation',
            name='short_desc',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
