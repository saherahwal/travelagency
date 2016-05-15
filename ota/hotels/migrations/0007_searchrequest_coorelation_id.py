# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_auto_20160503_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchrequest',
            name='coorelation_id',
            field=uuidfield.fields.UUIDField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
