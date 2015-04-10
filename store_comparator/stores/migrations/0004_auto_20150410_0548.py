# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_vende_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vende_producto',
            name='precio',
            field=models.DecimalField(max_digits=20, decimal_places=2),
            preserve_default=True,
        ),
    ]
