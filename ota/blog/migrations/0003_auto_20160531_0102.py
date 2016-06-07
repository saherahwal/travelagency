# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160530_2329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='body',
            new_name='blog_body',
        ),
    ]
