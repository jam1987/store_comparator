# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vende_producto',
            name='idCel',
        ),
        migrations.RemoveField(
            model_name='vende_producto',
            name='idTienda',
        ),
        migrations.DeleteModel(
            name='Vende_Producto',
        ),
        migrations.RemoveField(
            model_name='celular',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tienda',
            name='id',
        ),
        migrations.AddField(
            model_name='celular',
            name='idTienda',
            field=models.ManyToManyField(to='stores.Tienda'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='celular',
            name='precio',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='celular',
            name='idCel',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tienda',
            name='idTienda',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
