# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0006_auto_20150511_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='like',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='like',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='users',
        ),
        migrations.AlterUniqueTogether(
            name='profileuser',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='profileuser',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='profileuser',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='streamprofile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='streamprofile',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='streamprofile',
            name='stream',
        ),
        migrations.AlterUniqueTogether(
            name='viewer',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='profiles',
        ),
        migrations.AlterField(
            model_name='stream',
            name='archive',
            field=models.BooleanField(default=b'ARCHIVE_STREAMS'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='ProfileUser',
        ),
        migrations.DeleteModel(
            name='StreamProfile',
        ),
        migrations.DeleteModel(
            name='Viewer',
        ),
    ]
