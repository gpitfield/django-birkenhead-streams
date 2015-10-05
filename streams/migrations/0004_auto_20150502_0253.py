# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0003_auto_20150502_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamprofile',
            name='status',
            field=models.CharField(default=b'Invited', max_length=10, choices=[(b'Invited', b'Invited'), (b'Accepted', b'Accepted')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='role',
            field=models.CharField(default=b'Owner', max_length=10, choices=[(b'Owner', b'Owner')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stream',
            name='chat_key',
            field=models.CharField(db_index=True, unique=True, max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stream',
            name='publish_key',
            field=models.CharField(db_index=True, unique=True, max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stream',
            name='subscription_key',
            field=models.CharField(db_index=True, unique=True, max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
