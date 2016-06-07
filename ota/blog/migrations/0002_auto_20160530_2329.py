# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=models.ImageField(upload_to=b'blogs/images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blog',
            name='video_file',
            field=models.FileField(upload_to=b'blogs/videos/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blog',
            name='video_url',
            field=models.CharField(max_length=400, blank=True),
            preserve_default=True,
        ),
    ]
