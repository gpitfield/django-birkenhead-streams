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
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_value', models.TextField()),
                ('timestamp', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Like', max_length=10)),
                ('timestamp', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handle', models.CharField(max_length=15)),
                ('icon_key', models.URLField(default=b'http://tbd.com/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'Owner', max_length=10, choices=[(b'Owner', b'Owner'), (b'Identity', b'Identity')])),
                ('profile', models.ForeignKey(to='streams.Profile')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('publish_key', models.CharField(unique=True, max_length=32, db_index=True)),
                ('subscription_key', models.CharField(unique=True, max_length=32, db_index=True)),
                ('archive', models.BooleanField(default=True)),
                ('chat_key', models.CharField(unique=True, max_length=32, db_index=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'Scheduled', max_length=12, db_index=True, choices=[(b'Live', b'Live'), (b'Ended', b'Ended'), (b'Paused', b'Paused'), (b'Preload', b'Preload'), (b'Scheduled', b'Scheduled')])),
                ('duration', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Active', max_length=10, choices=[(b'Active', b'Active'), (b'Inactive', b'Inactive'), (b'Subscribed', b'Subscribed')])),
                ('timestamp', models.FloatField(default=0.0)),
                ('profile', models.ForeignKey(to='streams.Profile')),
                ('stream', models.ForeignKey(to='streams.Stream')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='viewer',
            unique_together=set([('profile', 'stream')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='streams.ProfileUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='profile',
            field=models.ForeignKey(to='streams.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='like',
            name='stream',
            field=models.ForeignKey(to='streams.Stream'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(to='streams.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='stream',
            field=models.ForeignKey(to='streams.Stream'),
            preserve_default=True,
        ),
    ]
