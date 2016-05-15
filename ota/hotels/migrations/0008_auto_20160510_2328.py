# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_searchrequest_coorelation_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booknowrequest',
            name='searchRequest',
        ),
        migrations.AddField(
            model_name='booknowrequest',
            name='coorelation_id',
            field=uuidfield.fields.UUIDField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
