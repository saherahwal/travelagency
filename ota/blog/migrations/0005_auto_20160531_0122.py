# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160531_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='embed_video_url',
            field=models.CharField(max_length=700, blank=True),
            preserve_default=True,
        ),
    ]
