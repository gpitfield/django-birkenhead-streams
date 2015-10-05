# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0004_auto_20150502_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='type',
            field=models.CharField(default=b'like', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='role',
            field=models.CharField(default=b'owner', max_length=10, choices=[(b'owner', b'owner'), (b'identity', b'identity')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stream',
            name='status',
            field=models.CharField(default=b'scheduled', max_length=12, db_index=True, choices=[(b'live', b'live'), (b'ended', b'ended'), (b'paused', b'paused'), (b'preload', b'preload'), (b'scheduled', b'scheduled')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stream',
            name='timestamp',
            field=models.DateTimeField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='streamprofile',
            name='role',
            field=models.CharField(default=b'primary', max_length=10, choices=[(b'primary', b'primary'), (b'secondary', b'secondary')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='streamprofile',
            name='status',
            field=models.CharField(default=b'invited', max_length=10, choices=[(b'invited', b'invited'), (b'accepted', b'accepted')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='viewer',
            name='status',
            field=models.CharField(default=b'active', max_length=10, choices=[(b'active', b'Active'), (b'inactive', b'inactive'), (b'subscribed', b'subscribed')]),
            preserve_default=True,
        ),
    ]
