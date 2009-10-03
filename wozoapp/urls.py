from django.conf.urls.defaults import *
from django.conf import settings
import os

urlpatterns = patterns('',
    (r'^$', 'wozo.wozoapp.views.index'),
    (r'^login/$', 'wozo.wozoapp.views.login'),
    (r'^logout/$', 'wozo.wozoapp.views.logout'),
    (r'^armar_resumen/$', 'wozo.wozoapp.views.armar_resumen'),
    (r'^armar_resumen/(?P<ordinal_dia>\d+)/$', 'wozo.wozoapp.views.armar_resumen'),
    (r'^menues_dias/$', 'wozo.wozoapp.views.menues_dias'),
    (r'^cargar_menu_dia/(?P<ordinal_dia>\d+)/$', 'wozo.wozoapp.views.cargar_menu_dia'),
    (r'^eliminar_menu_dia/(?P<menu_dia_id>\d+)/$', 'wozo.wozoapp.views.eliminar_menu_dia'),
    (r'^menues_normales/$', 'wozo.wozoapp.views.menues_normales'),
    (r'^eliminar_menu_normal/(?P<menu_normal_id>\d+)/$', 'wozo.wozoapp.views.eliminar_menu_normal'),
    (r'^pedir_menu/(?P<ordinal_dia>\d+)/$', 'wozo.wozoapp.views.pedir_menu'),
    (r'^eliminar_pedido/(?P<pedido_id>\d+)/$', 'wozo.wozoapp.views.eliminar_pedido'),
    #para usar archivos estaticos
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.MEDIA_ROOT, "wozoapp/")}),
)
