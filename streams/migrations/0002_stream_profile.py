# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='profile',
            field=models.ForeignKey(default=1, to='streams.Profile'),
            preserve_default=False,
        ),
    ]
