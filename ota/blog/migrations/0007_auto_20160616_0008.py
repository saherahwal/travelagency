# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_admin_visible_only'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='admin_visible_only',
            new_name='public',
        ),
    ]
