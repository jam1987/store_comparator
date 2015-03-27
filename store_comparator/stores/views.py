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

# Create your views here.

@csrf_protect
def index(request):
    return render_to_response('stores/home.html')


def buscar(request):
       if request.POST:
	       elemento = request.POST["nombre"]
       return render_to_response('stores/buscar.html',{'mensaje':'busqueda realizada','buscado':elemento,},context_instance=RequestContext(request))
	