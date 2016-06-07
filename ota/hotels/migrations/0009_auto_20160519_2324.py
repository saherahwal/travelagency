# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_auto_20160510_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='city',
            field=models.CharField(max_length=120),
            preserve_default=True,
        ),
    ]
