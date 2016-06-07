# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0014_topinterestlocations'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TopInterestLocations',
            new_name='TopInterestLocation',
        ),
    ]
