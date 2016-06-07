# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160531_0102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='video_url',
            new_name='embed_video_url',
        ),
    ]
