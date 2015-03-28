# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vende_producto',
            name='direccion',
            field=models.URLField(max_length=200000, default=''),
            preserve_default=False,
        ),
    ]
