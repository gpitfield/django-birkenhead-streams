# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0002_stream_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'Primary', max_length=10, choices=[(b'Primary', b'Primary'), (b'Secondary', b'Secondary')])),
                ('profile', models.ForeignKey(to='streams.Profile')),
                ('stream', models.ForeignKey(to='streams.Stream')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='streamprofile',
            unique_together=set([('profile', 'stream')]),
        ),
        migrations.RemoveField(
            model_name='stream',
            name='profile',
        ),
        migrations.AddField(
            model_name='stream',
            name='profiles',
            field=models.ManyToManyField(to='streams.Profile', through='streams.StreamProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='handle',
            field=models.CharField(unique=True, max_length=15),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='profileuser',
            unique_together=set([('profile', 'user')]),
        ),
    ]
