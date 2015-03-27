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
from django.db import IntegrityError
from django.db import DatabaseError
import requests
import urllib
from bs4 import BeautifulSoup

# Create your views here.

@csrf_protect
def index(request):
    return render_to_response('stores/home.html')


def buscar(request):
       if request.POST:
           elemento = request.POST["nombre"]
           web = "http://listado.mercadolibre.com.co/"+elemento
           direccion = ''.join(web)
           informacion = requests.get(direccion)
           scrapping = BeautifulSoup(informacion.text)
           info_producto = scrapping.find(id="searchResults")
           contenido = info_producto.a 
           enlace = contenido["href"]
           nombre = ''
           for elem in contenido.contents:
               nombre = nombre + str(elem) 
           nombre_producto_old1 = ''.join(nombre)
           nombre_producto_old = nombre_producto_old1.replace("<strong>","")
           nombre_producto = nombre_producto_old.replace("</strong>","")
           monto_texto = info_producto.div 	
           monto_1 = monto_texto.div
           monto = str(monto_1.strong.contents[0])
       return render_to_response('stores/buscar.html',{'mensaje':'busqueda realizada','enlace':enlace,'nombre_producto':nombre_producto,'monto':monto},context_instance=RequestContext(request))
	