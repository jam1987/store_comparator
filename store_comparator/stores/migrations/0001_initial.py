# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Celular',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idCel', models.CharField(max_length=200)),
                ('nombreCel', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idTienda', models.CharField(max_length=200)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.DecimalField(max_digits=10, decimal_places=2)),
                ('idCel', models.ForeignKey(to='stores.Celular')),
                ('idTienda', models.ForeignKey(to='stores.Tienda')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
