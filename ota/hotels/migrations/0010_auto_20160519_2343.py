# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_auto_20160519_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='city',
            field=models.CharField(max_length=93),
            preserve_default=True,
        ),
    ]
