# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('nombreProducto', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('idTienda', models.CharField(primary_key=True, serialize=False, max_length=200)),
                ('nombreTienda', models.CharField(max_length=200)),
                ('direccion', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vende_Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('precio', models.CharField(max_length=200)),
                ('idProducto', models.ForeignKey(to='stores.Producto')),
                ('idTienda', models.ForeignKey(to='stores.Tienda')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vende_producto',
            unique_together=set([('idTienda', 'idProducto')]),
        ),
        migrations.AddField(
            model_name='tienda',
            name='dispositivos',
            field=models.ManyToManyField(through='stores.Vende_Producto', to='stores.Producto'),
            preserve_default=True,
        ),
    ]
