# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('body', models.TextField()),
                ('short_desc', models.CharField(max_length=600)),
                ('img', models.ImageField(upload_to=b'blogs/images/')),
                ('video_file', models.FileField(upload_to=b'blogs/videos/')),
                ('video_url', models.CharField(max_length=400)),
                ('blog_by', models.ForeignKey(related_name='blog_by_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=None,
            managers=None,
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
            preserve_default=True,
        ),
    ]
