# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_remove_scores_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='scores',
            name='hotel',
            field=models.ForeignKey(related_name='hotel', default=None, to='hotels.Hotel'),
            preserve_default=False,
        ),
    ]
