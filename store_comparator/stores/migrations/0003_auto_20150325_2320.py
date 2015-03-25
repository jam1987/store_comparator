# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20150325_2258'),
    ]

    operations = [
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
        migrations.AlterUniqueTogether(
            name='vende_producto',
            unique_together=set([('idTienda', 'idCel')]),
        ),
        migrations.RemoveField(
            model_name='celular',
            name='idTienda',
        ),
        migrations.RemoveField(
            model_name='celular',
            name='precio',
        ),
        migrations.AddField(
            model_name='tienda',
            name='dispositivos',
            field=models.ManyToManyField(to='stores.Celular', through='stores.Vende_Producto'),
            preserve_default=True,
        ),
    ]
