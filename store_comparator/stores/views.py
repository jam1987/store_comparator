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
from stores.models import Tienda, Vende_Producto
from django.db import IntegrityError
from django.db import DatabaseError
import requests
import urllib
from bs4 import BeautifulSoup
from tasks import add, mul, xsum, buscar
# Create your views here.

@csrf_protect
def index(request):
    return render_to_response('stores/home.html')


def recibir_parametro(request):
       if request.POST:
           elemento = request.POST["nombre"]
           tiendas = get_object_or_404(Tienda,idTienda ='LN01')
           result = buscar(elemento,tiendas)
           tiendas = get_object_or_404(Tienda,idTienda ='ML01')
           result = buscar(elemento,tiendas)
           tiendas = get_object_or_404(Tienda,idTienda ='EX01')
           result = buscar(elemento,tiendas)
           
       ventas = Vende_Producto.objects.all().order_by('-precio')
       
       producto = []
       i = 0
     
           
  
       return render_to_response('stores/buscar.html',{'mensaje':'busqueda realizada','ventas':ventas,},context_instance=RequestContext(request))
	   

	