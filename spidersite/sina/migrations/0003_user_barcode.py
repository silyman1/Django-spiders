# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0002_user_brief'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='barcode',
            field=models.CharField(default=b'weixin.jpg', max_length=200),
        ),
    ]
