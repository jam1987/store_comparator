# Nombre del Archivo:  views.py
# Descripcion del Archivo: Este archivo contiene los metodos principales de la Aplicacion
#                          store_comparator. Estos metodos corresponden al controlador de
#                          la misma.
# Version: 1.0
# Autor: Julio De Abreu Molina
# Fecha de Finalizacion: 31 de Marzo del 2014

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.db import transaction
from stores.models import Tienda, Vende_Producto, Producto
from django.db import IntegrityError
from django.db import DatabaseError
import requests
import urllib
from bs4 import BeautifulSoup
from tasks import buscar
import gevent
# Create your views here.

# Nombre del Metodo: Index
# Parametros de entrada: Request - Corresponde a los datos de
#                                  la sesion en curso
# Parametros de salida: Home.html - Corresponde a la pagina principal
# Descripcion: Este metodo es usado para disparar la pagina principal.
@csrf_protect
def index(request):
    return render_to_response('stores/home.html')


# Nombre del Metodo: Recibir_Parametro
# Parametros de Entrada: Request - Corresponde a los datos de
#                                  la sesion en curso
# Parametros de salida: Buscar.html - Corresponde a la pagina en la cual
#                                     se mostraran los resultados
# Descripcion del metodo: Este metodo es empleado para realizar la busqueda
#                         del producto en cuatro sitios de forma concurrente:
#                         Mercado Libre, Linio, OLX y Exito	
def recibir_parametro(request):       
       if request.POST:
           elemento = request.POST["nombre"]
		   
		   # Se borra el historial previo de productos y ventas
           ventas = Vende_Producto.objects.all()
           for venta in ventas:
               venta.delete()
           productos = Producto.objects.all()
           for producto in productos:
                producto.delete()		   
           tiendas = get_object_or_404(Tienda,idTienda ='LN01')
           tupla1 = (elemento,tiendas.nombreTienda,tiendas.direccion)
           tiendas = get_object_or_404(Tienda,idTienda ='ML01')
           tupla2 = (elemento,tiendas.nombreTienda,tiendas.direccion)
           tiendas = get_object_or_404(Tienda,idTienda ='OL01')
           print(tiendas.direccion)         
           tupla3 = (elemento,tiendas.nombreTienda,tiendas.direccion)
           tiendas = get_object_or_404(Tienda,idTienda ='EX01')
           tupla4 = (elemento,tiendas.nombreTienda,tiendas.direccion,'X')
		
           tuplas = [tupla1,tupla2,tupla3,tupla4]
		   
		   # Se ejecuta la funcion Buscar de forma recurrente. Los resultados se pueden ver
		   # en Celery
           jobs = [gevent.spawn(buscar.delay,tupla) for tupla in tuplas]
           gevent.joinall(jobs,timeout=20)
           ventas = Vende_Producto.objects.all().order_by('-precio')
       return render_to_response('stores/buscar.html',{'mensaje':'busqueda realizada','ventas':ventas,},context_instance=RequestContext(request))
	   
# Nombre del Metodo: Compartir
# Parametros de Entrada: Request - Corresponde a los datos de
#                                  la sesion en curso
# Parametros de salida: Compartir.html - Corresponde a la pagina en la cual
#                                     se mostraran los resultados buscados anteriormente
# Descripcion del metodo: Este metodo es empleado para mostrar los resultados en forma
#                         ordenada para compartirlos con otras personas
def compartir(request):
    ventas = Vende_Producto.objects.all().order_by('-precio')
    return render_to_response('stores/compartir.html',{'mensaje':'busqueda realizada','ventas':ventas,},context_instance=RequestContext(request))
