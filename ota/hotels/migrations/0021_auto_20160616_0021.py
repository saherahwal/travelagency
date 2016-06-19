# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0020_topinterestlocation_admin_visible_only'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topinterestlocation',
            old_name='admin_visible_only',
            new_name='public',
        ),
    ]
