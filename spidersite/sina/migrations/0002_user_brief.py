# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='brief',
            field=models.CharField(default=b'\xe6\x9a\x82\xe6\x97\xa0', max_length=200),
        ),
    ]
