from django.db import models
class Celular(models.Model):
    idCel = models.CharField(max_length=200)
    nombreCel = models.CharField(max_length=200)
        
class Tienda(models.Model):
    idTienda = models.CharField(max_length=200)
    nombreTienda = models.CharField(max_length=200)
    direccion = models.URLField(max_length=200)

class Vende_Producto(models.Model):
    idTienda = models.ForeignKey(Tienda)
    idCel = models.ForeignKey(Celular)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
