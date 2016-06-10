# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0015_auto_20160529_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='topinterestlocation',
            name='img',
            field=models.ImageField(upload_to=b'topinterests/images/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topinterestlocation',
            name='topinterests_body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
