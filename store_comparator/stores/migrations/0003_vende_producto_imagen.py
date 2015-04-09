# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_vende_producto_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='vende_producto',
            name='imagen',
            field=models.URLField(default='', max_length=2000000),
            preserve_default=False,
        ),
    ]
