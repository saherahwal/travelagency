# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160531_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='admin_visible_only',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
