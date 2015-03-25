from django.db import models

class Celular(models.Model):
    idCel = models.CharField(max_length=200,primary_key=True)
    nombreCel = models.CharField(max_length=200)


class Tienda(models.Model):
    idTienda = models.CharField(max_length=200,primary_key=True)
    nombreTienda = models.CharField(max_length=200)
    direccion = models.URLField(max_length=200)
    dispositivos = models.ManyToManyField(Celular,through='Vende_Producto',through_fields=('idTienda','idCel'))


class Vende_Producto(models.Model):
    idTienda = models.ForeignKey(Tienda)
    idCel = models.ForeignKey(Celular)
    precio = models.DecimalField(max_digits=10, decimal_places=2)       
    
    class Meta:
        unique_together = (("idTienda","idCel"),)
