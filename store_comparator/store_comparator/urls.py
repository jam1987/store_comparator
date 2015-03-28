from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'store_comparator.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'index/','stores.views.index'),
	url(r'recibir_parametro/', 'stores.views.recibir_parametro'),
	url(r'mostrar_resultados/','stores.views.recibir_parametro'),
    url(r'^admin/', include(admin.site.urls)),
)
