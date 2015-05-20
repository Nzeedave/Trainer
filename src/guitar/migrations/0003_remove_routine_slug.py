# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guitar', '0002_auto_20150517_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='slug',
        ),
    ]
