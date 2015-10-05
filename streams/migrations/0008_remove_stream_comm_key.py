# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0007_auto_20150529_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='comm_key',
        ),
    ]
