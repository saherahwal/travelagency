# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0019_auto_20160611_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='topinterestlocation',
            name='admin_visible_only',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
