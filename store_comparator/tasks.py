from __future__ import absolute_import
from django.shortcuts import render
from stores.models import *
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
from bs4 import BeautifulSoup
from store_comparator.celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y

@app.task
def buscar(elemento, tienda):
    info = ()
    if tienda.nombreTienda == 'Mercado Libre':
       info = get_info_m_l(tienda.direccion,elemento)
    elif tienda.nombreTienda == 'ÓLX':
       info = get_info_olx(tienda.direccion,elemento)
    elif tienda.nombreTienda == 'Linio':
       info = get_info_linio(tienda.direccion,elemento)
    elif tienda.nombreTienda == 'Exito':
       info = get_info_exito(tienda.direccion,elemento)
		
    try:
        prod = Producto.objects.create(
		    
		    idProducto = info[3],
			nombreProducto = info[1]
	    )
        prod.save()	
        
        vende = Vende_Producto.objects.create(
            idProducto = prod,
            idTienda = tienda,
            precio = info[2],
		    direccion = info[3]
        )
        vende.save()
    except IntegrityError:
        transaction.rollback()
        return 1
    return 0
	
def get_info_m_l(direccion,elemento):
    web = direccion+elemento
    direccion = ''.join(web)
    informacion = requests.get(direccion)
    scrapping = BeautifulSoup(informacion.text)
    info_producto = scrapping.find(id="searchResults")
    contenido = info_producto.a 
    enlace = contenido["href"]
    nombre = ''
    nombre_producto = ''
    monto = ''
    id = ''
    for elem in contenido.contents:
        nombre = nombre + str(elem) 
        nombre_producto_old1 = ''.join(nombre)
        nombre_producto_old = nombre_producto_old1.replace("<strong>","")
        nombre_producto = nombre_producto_old.replace("</strong>","")
        monto_texto = info_producto.div 	
        monto_1 = monto_texto.div
        monto = str(monto_1.strong.contents[0])
        i=0
        id =  nombre_producto[0:2]+str(i)
        i = i + 1
        id = ''.join(id)	
    return (enlace,nombre_producto,monto,id)		

def get_info_linio(direccion,elemento):
    web = direccion+elemento
    direccion = ''.join(web)
    informacion = requests.get(direccion)
    scrapping = BeautifulSoup(informacion.text)
    info_producto = scrapping.find(id="catalog-content")
    contenido = info_producto.a 
    enlace = contenido["href"]
    nombre_producto = contenido["title"]
    monto = contenido.li.find_next("li").find_next("li").find_next("li").span.find_next("span").contents[0]
    i = 1
    id = nombre_producto[0:2]+str(i)
    return (enlace,nombre_producto,monto,id)

def get_info_olx(direccion,elemento):
    # web = tienda.direccion+elemento
    # direccion = ''.join(web)
    # informacion = requests.get(direccion)
    # scrapping = BeautifulSoup(informacion.text)
    # info_producto = scrapping.find(id="searchResults")
    # contenido = info_producto.a 
    # enlace = contenido["href"]
    # nombre = ''
	# nombre_producto = ''
	# monto = ''
	# id = ''
    # for elem in contenido.contents:
        # nombre = nombre + str(elem) 
        # nombre_producto_old1 = ''.join(nombre)
        # nombre_producto_old = nombre_producto_old1.replace("<strong>","")
        # nombre_producto = nombre_producto_old.replace("</strong>","")
        # monto_texto = info_producto.div 	
        # monto_1 = monto_texto.div
        # monto = str(monto_1.strong.contents[0])
        # i=0
        # id =  nombre_producto[0:2]+str(i)
        # i = i + 1
        # id = ''.join(id)	
    return ()

def get_info_exito(direccion,elemento):
    web = direccion+elemento
    direccion = ''.join(web)
    informacion = requests.get(direccion)
    scrapping = BeautifulSoup(informacion.text)
    info_producto = scrapping.find(id="plpContent")
    contenido = info_producto.div
    enlace = "www.exito.com/"+info_producto.a["href"]
    enlace = ''.join(enlace)
    nombre_producto = contenido.h2.contents[0]
    monto = contenido.h4.contents[0].replace("\n\t\t\t\t\t\t","")
    i = 2
    id = nombre_producto[0:2]+str(i)
    id = ''.join(id)	
    return (enlace,nombre_producto,monto,id)
		
@app.task
def xsum(numbers):
    return sum(numbers)