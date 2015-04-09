# Nombre del Archivo:  tasks.py
# Descripcion del Archivo: Este archivo contiene los metodos que se van a aplicar
#                          de manera concurrente.
# Version: 1.0
# Autor: Julio De Abreu Molina
# Fecha de Finalizacion: 31 de Marzo del 2014

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
import pusher
from bs4 import BeautifulSoup
from store_comparator.celery import app
import socket


# Nombre de la Funcion: Buscar
# Parametros de entrada: Tupla - Corresponde a una 3-tupla la cual contie-
#                        ne la siguiente informacion:
#                        1) El elemento a buscar
#                        2) El nombre de la Tienda
#                        3) La direccion Web de la tienda 
# Parametros de salida: 1 o 0. Sin embargo la funcion envia los resultados
#                       a traves de la interfaz de Pusher y HTTP de Python.
# Descripcion: Esta funcion se encarga de realizar la busqueda de la infor-
#              macion del producto.
@app.task
def buscar(tupla):
    info = ()
    if tupla[1] == 'Mercado Libre':
       info = get_info_m_l(tupla[2],tupla[0])
    elif tupla[1] == 'OLX':
       info = get_info_olx(tupla[2],tupla[0])
    elif tupla[1] == 'Linio':
       info = get_info_linio(tupla[2],tupla[0])
    elif tupla[1] == 'Exito':
       info = get_info_exito(tupla[2],tupla[0])
		
    try: 
	
	    # Se crean dos objetos: Producto y Vende_Producto
        prod = Producto.objects.create(
		    idProducto = info[3],
			nombreProducto = info[1]
	    )
        prod.save()	
        
        tienda = get_object_or_404(Tienda,nombreTienda=tupla[1])
        vende = Vende_Producto.objects.create(
            idProducto = prod,
            idTienda = tienda,
            precio = info[2],
		    direccion = info[0],
            imagen = info[3]
        )
        vende.save()
		
		# Se crea la instancia Pusher 
        p = pusher.Pusher(
            app_id='113190',
            key='8ab69fb95f1656821b78',
            secret='7d2e9bf083500c9b00de'
        )
        nombre = prod.nombreProducto
        precio = vende.precio
        nombreTienda = tienda.nombreTienda
        direccion = vende.direccion
	imagen = vende.imagen	
		# Se envian los datos
        p['test_channel'].trigger('my_event', {'message': nombre, 'message1':precio,'message2':nombreTienda, 'message3':direccion,'message4':imagen})
   
    except IntegrityError:
        transaction.rollback()
        return 1
    return 0
	

# Nombre de la Funcion: Get_info_m_l
# Parametros de entrada: - Direccion: Corresponde a la URL de Mercado Libre
#                        - Elemento: Corresponde al producto
# Parametros de salida: Tupla - Corresponde a una 4-tupla la cual contiene 
#                       la siguiente informacion:
#                       1) Enlace: Corresponde al enlace del sitio web con 
#                                  informacion del producto
#                       2) nombre_producto: Nombre del producto en el sitio
#                                           Web
#                       3) Monto: Corresponde al precio del producto en la 
#                                 tienda
#                       4) Id: Identificador creado para el producto
# Descripcion: Esta funcion se encarga de realizar la busqueda de la infor-
#              macion del producto en Mercado Libre. Para eso se realiza 
#              el request y luego el Scrapping a traves de BeautifulSoup
#              para obtener los datos 
def get_info_m_l(direccion,elemento):
    web = direccion+elemento
    direccion = ''.join(web)
    informacion = requests.get(direccion)
    if informacion.status_code == 200:
        scrapping = BeautifulSoup(informacion.text)
        info_producto = scrapping.find(id="searchResults")
        contenido = info_producto.a 
        enlace = contenido["href"]
        # imagen = contenido.img["src"]
        nombre = ''
        nombre_producto = ''
        monto = ''
        id = ''
        for elem in contenido.contents:
            nombre = nombre + elem.encode('utf-8') 
            nombre_producto_old1 = ''.join(nombre)
            nombre_producto_old = nombre_producto_old1.replace("<strong>","")
            nombre_producto = nombre_producto_old.replace("</strong>","")
        monto_texto = info_producto.div 	
        monto_1 = monto_texto.div
        monto = (monto_1.strong.contents[0].encode('utf-8')).replace("$\xc2\xa0","")
        i=0
        id =  nombre_producto[0:2]+str(i)
        i = i + 1
        id = ''.join(id)	
    else:
        nombre_producto = elemento
        id = nombre_producto[0:2]
        monto = "Fallo"
        enlace = ""
        imagen = ""
    return (enlace,nombre_producto,monto,id,"")	

	
# Nombre de la Funcion: Get_info_linio
# Parametros de entrada: - Direccion: Corresponde a la URL de Linio
#                        - Elemento: Corresponde al producto
# Parametros de salida: Tupla - Corresponde a una 4-tupla la cual contiene 
#                       la siguiente informacion:
#                       1) Enlace: Corresponde al enlace del sitio web con 
#                                  informacion del producto
#                       2) nombre_producto: Nombre del producto en el sitio
#                                           Web
#                       3) Monto: Corresponde al precio del producto en la 
#                                 tienda
#                       4) Id: Identificador creado para el producto
# Descripcion: Esta funcion se encarga de realizar la busqueda de la infor-
#              macion del producto en Linio. Para eso se realiza 
#              el request y luego el Scrapping a traves de BeautifulSoup
#              para obtener los datos 
def get_info_linio(direccion,elemento):
    web = direccion+elemento
    direccion = ''.join(web)
    enlace = ""
    imagen = ""
    informacion = requests.get(direccion)
    scrapping = BeautifulSoup(informacion.text)
    not_found = scrapping.find(id="not-found-container")
    if not_found is None:
        info_producto = scrapping.find(id="catalog-content")
        if info_producto is None:
           monto = "Fallo"
           i = 1
           nombre_producto = elemento
           id = nombre_producto[0:2]+str(i)
        else:
            contenido = info_producto.a 
            monto = ""
            id = ""
            enlace = contenido["href"]
            nombre_producto = contenido["title"]
            #imagen = contenido.li.span.span.img["src"]
            monto_aux = contenido.li.find_next("li").find_next("li").find_next("li").span.find_next("span")
            if len(monto_aux.contents) > 0:
                monto = monto_aux.contents[0]
            else:
                 monto = "Fallo"
                 i = 1
                 nombre_producto = elemento
                 id = nombre_producto[0:2]+str(i)	
    else:	
        monto = "No Encontrado"
        i = 1
        nombre_producto = elemento
        id = nombre_producto[0:2]+str(i)	
    return (enlace,nombre_producto,monto,id,"")

# Nombre de la Funcion: Get_info_olx
# Parametros de entrada: - Direccion: Corresponde a la URL de OLX
#                        - Elemento: Corresponde al producto
# Parametros de salida: Tupla - Corresponde a una 4-tupla la cual contiene 
#                       la siguiente informacion:
#                       1) Enlace: Corresponde al enlace del sitio web con 
#                                  informacion del producto
#                       2) nombre_producto: Nombre del producto en el sitio
#                                           Web
#                       3) Monto: Corresponde al precio del producto en la 
#                                 tienda
#                       4) Id: Identificador creado para el producto
# Descripcion: Esta funcion se encarga de realizar la busqueda de la infor-
#              macion del producto en OLX. Para eso se realiza 
#              el request y luego el Scrapping a traves de BeautifulSoup
#              para obtener los datos 
def get_info_olx(direccion,elemento):
    header = {'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'es-ES,es;q=0.8,en;q=0.6',
 'Connection': 'keep-alive',
 'Content-Type': 'text/html',
 'Origin': 'http://olx.com.co',
 'Referer': 'http://olx.com.co',
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
    web = direccion+elemento
    direccion = ''.join(web)
    informacion = requests.get(direccion,headers=header)
    
    
    scrapping = BeautifulSoup(informacion.text)
    info_producto = scrapping.find(id="listing-items")
    enlace = ""
    contenido = info_producto.find_next("ul").find_next("ul").find_next("ul").find_next("ul").find_next("ul")
    enlace = contenido.li.a["href"]
    imagen = str(contenido.li.a.figure.img["src"])
    print(imagen)
    nombre_producto = (contenido.li.h3.contents[0].encode("utf-8")).replace("\xc2\xa1","")
    monto = (str(contenido.li.p.contents[0]).replace(" ","")).replace("\n","")
    id = ''
    i=3
    id =  nombre_producto[0:2]+str(i)
    id = ''.join(id)	
    return (enlace,nombre_producto,monto,id,imagen)

# Nombre de la Funcion: Get_info_exito
# Parametros de entrada: - Direccion: Corresponde a la URL de Exito
#                        - Elemento: Corresponde al producto
# Parametros de salida: Tupla - Corresponde a una 4-tupla la cual contiene 
#                       la siguiente informacion:
#                       1) Enlace: Corresponde al enlace del sitio web con 
#                                  informacion del producto
#                       2) nombre_producto: Nombre del producto en el sitio
#                                           Web
#                       3) Monto: Corresponde al precio del producto en la 
#                                 tienda
#                       4) Id: Identificador creado para el producto
# Descripcion: Esta funcion se encarga de realizar la busqueda de la infor-
#              macion del producto en Exito. Para eso se realiza 
#              el request y luego el Scrapping a traves de BeautifulSoup
#              para obtener los datos 
def get_info_exito(direccion,elemento):
    web = direccion+elemento
    direccion = ''.join(web)
    informacion = requests.get(direccion)
    datos = BeautifulSoup(informacion.text)
    monto = ""
    imagen = ""
    info_producto = datos.find(id="plpContent")
	
    if  info_producto is None:       
        nombre_producto = elemento
        monto = "Fallo"
        enlace = ""
        i = 2
        id = nombre_producto[0:2]+str(i)
        id = ''.join(id)
    else:
         contenido = info_producto.div
         enlace = "www.exito.com"+info_producto.a["href"]
         enlace = ''.join(enlace)
         # imagen = info_producto.img["src"]
         nombre_producto = contenido.h2.contents[0]
         monto = contenido.h4.contents[0].replace("\n\t\t\t\t\t\t","")
         i = 2
         id = nombre_producto[0:2]+str(i)
         id = ''.join(id)
        
    return (enlace,nombre_producto,monto,id,"")
		
@app.task
def xsum(numbers):
    return sum(numbers)
