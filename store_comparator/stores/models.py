from django.db import models

class Producto(models.Model):
    idProducto = models.CharField(max_length=200,primary_key=True)
    nombreProducto = models.CharField(max_length=200)


class Tienda(models.Model):
    idTienda = models.CharField(max_length=200,primary_key=True)
    nombreTienda = models.CharField(max_length=200)
    direccion = models.URLField(max_length=200)
    dispositivos = models.ManyToManyField(Producto,through='Vende_Producto',through_fields=('idTienda','idProducto'))


class Vende_Producto(models.Model):
    idTienda = models.ForeignKey(Tienda)
    idProducto = models.ForeignKey(Producto)
    precio = models.CharField(max_length=200)       
    
    class Meta:
        unique_together = (("idTienda","idProducto"),)
