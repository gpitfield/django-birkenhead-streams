# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0005_auto_20150510_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stream',
            old_name='chat_key',
            new_name='comm_key',
        ),
    ]
