from wozo.wozoapp.models import Pedido, MenuNormal, MenuDia
from forms import LoginForm, MenuDiaForm, MenuNormalForm, PedidoForm
from utiles import *

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import django.contrib.auth

from datetime import date, datetime
import random


@login_required
def index(request):
    "Pagina principal"

    pedidos_dias = []
    mensajes = []

    hoy = date.today()

    #armar lista de dias, con los pedidos de cada dia
    #estructura: (titulo de la seccion, fecha, es hoy, dia de semana, pedidos, editables o no)
    for numero, fecha, dia_semana, semana in obtener_dias():
        titulo = ""
        if numero == 0:
            titulo = "Esta Semana"
        elif numero == 7:
            titulo = "Semana Proxima"
        
        pedidos_dias.append((titulo,
                             fecha,
                             fecha == hoy,
                             dia_semana,
                             Pedido.objects.filter(user=request.user,
                                                   dia=fecha
                                                   ).order_by('dia'),
                             fecha >= hoy))
    
    cantidad_faltante = len([x for x in pedidos_dias if len(x[3]) == 0])
    if cantidad_faltante:
        mensajes.append("Fijate que hay %i dias sin menu pedido." % cantidad_faltante)
    
        #el menu random del dia
    sugerencia_random = "Nada (No hay menues normales de donde sacar una)"
    if MenuNormal.objects.count():
        sugerencia_random = MenuNormal.objects.all()[date.today().toordinal() % MenuNormal.objects.count()].nombre

    #sugerencia de algo que nunca comiste
    sugerencia_nueva = "Nada (No hay menues normales de donde sacar una)"
    hoy = date.today()
    if MenuNormal.objects.count():
        menues_nuevos = [m.nombre for m in MenuNormal.objects.all()
                         if m.pedido_set.filter(user=request.user).count() == 0]
        if menues_nuevos:
            sugerencia_nueva = random.choice(menues_nuevos)

    return render_to_response('wozoapp/index.html', {'pedidos_dias': pedidos_dias,
                                                     'mensajes': mensajes,
                                                     'sugerencia_random': sugerencia_random,
                                                     'sugerencia_nueva': sugerencia_nueva,
                                                     'user': request.user,
                                                     'root_url': root_url,
                                                     'actual_url': request.path,})

@login_required    
def pedir_menu(request, ordinal_dia):
    "Pedir menu para un dia determinado"
    dia = date.fromordinal(int(ordinal_dia))
    pedido_form = PedidoForm()
    error = None
    if request.method == 'POST':
        menu_normal = request.POST['menu_normal']
        menu_dia = request.POST['menu_dia']
        menu_especial = request.POST['menu_especial']
        pidio = False
        
        if menu_normal and (int(menu_normal) > -1):
            pidio = True
            pedido = Pedido()
            pedido.user = request.user
            pedido.dia = dia
            pedido.menu_normal = MenuNormal.objects.get(id=menu_normal)
            pedido.save()
        
        if menu_dia and (int(menu_dia) > -1):
            pidio = True
            pedido = Pedido()
            pedido.user = request.user
            pedido.dia = dia
            pedido.menu_dia = MenuDia.objects.get(id=menu_dia)
            pedido.save()
        
        if menu_especial and (len(menu_especial.strip()) > 0):
            pidio = True
            pedido = Pedido()
            pedido.user = request.user
            pedido.dia = dia
            pedido.menu_especial = menu_especial
            pedido.save()

        if pidio:
            return HttpResponseRedirect(request.GET['next'])
        else:
            pedido_form = PedidoForm(request.POST)
            error = "Che, faltan completar algunas cosas."

    pedido_form.fields['menu_dia'].choices = [(-1, '<< No pido menu del dia, voy a pedir otra cosa >>')]
    pedido_form.fields['menu_dia'].choices.extend([(menu.id, menu.nombre + ": " + menu.contenido)
                                                   for menu in MenuDia.objects.filter(dia=dia).order_by("nombre")])
    
    pedido_form.fields['menu_normal'].choices = [(-1, '<< No pido menu normal, voy a pedir otra cosa >>')]
    pedido_form.fields['menu_normal'].choices.extend([(menu.id, menu.nombre + ": " + menu.contenido)
                                                      for menu in MenuNormal.objects.all().order_by("nombre")])
    
    dia_semana = DIAS_SEMANA[dia.weekday()]
    pedidos = Pedido.objects.filter(user=request.user, dia=dia).order_by('dia')

    return render_to_response('wozoapp/pedir_menu.html', {'pedido_form': pedido_form,
                                                          'dia_ordinal': dia.toordinal(),
                                                          'dia': dia,
                                                          'dia_semana': dia_semana,
                                                          'pedidos': pedidos,
                                                          'user': request.user,
                                                          'root_url': root_url,
                                                          'actual_url': request.path,
                                                          'error': error})


@login_required
def eliminar_pedido(request, pedido_id):
    "Elimina un pedido de menu"
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    pedido.delete()
    return HttpResponseRedirect(request.GET['next'])
    
@login_required    
def armar_resumen(request, ordinal_dia=date.today().toordinal()):
    "Armar resumen de pedidos de los usuarios para un dia"

    dias = [(ds, f.toordinal()) for n, f, ds, s in obtener_dias()]

    titulo_dia = [nombre for nombre, ordinal in dias
                      if ordinal == int(ordinal_dia)]
    if titulo_dia:
        titulo_dia = titulo_dia[0]
    else:
        titulo_dia = "Para hoy no se deberia pedir menu"
    
    dia = date.fromordinal(int(ordinal_dia))

    longitud = len(dias) / 2
    #agrupar por dias iguales de distintas semanas:
    #(lunes, lunes prox), (martes, martes prox) ...
    dias = [(dias[i][0], dias[i][1], dias[i + longitud][0], dias[i + longitud][1])
            for i in range(longitud)]


    menues_dias = [(md, md.pedido_set.count())
                   for md in MenuDia.objects.filter(dia=dia)
                   if md.pedido_set.count() > 0]
        
    menues_normales = [(mn, mn.pedido_set.filter(dia=dia).count())
                       for mn in MenuNormal.objects.all()
                       if mn.pedido_set.filter(dia=dia).count() > 0]
        
    menues_especiales = [p.menu_especial
                         for p in Pedido.objects.filter(dia=dia)
                         if p.menu_especial and len(p.menu_especial.strip()) > 0]
   
    usuarios_sin_pedido = [usuario.username for usuario in User.objects.all()
                           if usuario.pedido_set.filter(dia=dia).count() == 0]
   
    return render_to_response('wozoapp/armar_resumen.html', {'menues_dias': menues_dias,
                                                             'menues_normales': menues_normales,
                                                             'menues_especiales': menues_especiales,
                                                             'usuarios_sin_pedido': ", ".join(usuarios_sin_pedido),
                                                             'titulo_dia': titulo_dia,
                                                             'dia': dia,
                                                             'dias': dias,
                                                             'user': request.user,
                                                             'root_url': root_url})

@login_required    
def menues_dias(request):
    "Abm de los menues de cada dia"
    
    hoy = date.today()

    menues_dias = []
    
    #armar lista de dias, con los menues de cada dia
    #estructura: (titulo de la seccion, fecha, dia de semana, pedidos, editables o no)
    for numero, fecha, dia_semana, semana in obtener_dias():
        titulo = ""
        if numero == 0:
            titulo = "Esta Semana"
        elif numero == 7:
            titulo = "Semana Proxima"
        
        menues_dias.append((titulo,
                            fecha,
                            fecha == hoy,
                            dia_semana,
                            MenuDia.objects.filter(dia=fecha).order_by('nombre'),
                            fecha >= hoy))

    return render_to_response('wozoapp/menues_dias.html', {'menues_dias': menues_dias,
                                                           'user': request.user,
                                                           'root_url': root_url,
                                                           'actual_url': request.path,})

@login_required    
def cargar_menu_dia(request, ordinal_dia):
    "Carga un menu para un dia determinado"
    dia = date.fromordinal(int(ordinal_dia))
    menu_dia_form = MenuDiaForm()
    error = None
    if request.method == 'POST':
        nombre = request.POST['nombre']
        contenido = request.POST['contenido']
        if nombre and contenido:
            menu_dia = MenuDia()
            menu_dia.dia = dia
            menu_dia.nombre = nombre
            menu_dia.contenido = contenido
            menu_dia.save()
            return HttpResponseRedirect(request.GET['next'])
        else:
            menu_dia_form = MenuDiaForm(request.POST)
            error = "Che, faltan completar algunas cosas."

    dia_semana = DIAS_SEMANA[dia.weekday()]
    menues = MenuDia.objects.filter(dia=dia).order_by('nombre')

    return render_to_response('wozoapp/cargar_menu_dia.html', {'menu_dia_form': menu_dia_form,
                                                               'dia_ordinal': dia.toordinal(),
                                                               'dia': dia,
                                                               'dia_semana': dia_semana,
                                                               'menues': menues,
                                                               'user': request.user,
                                                               'root_url': root_url,
                                                               'actual_url': request.path,
                                                               'error': error})

@login_required
def eliminar_menu_dia(request, menu_dia_id):
    "Elimina un menu del dia"
    menu_dia = get_object_or_404(MenuDia, pk=menu_dia_id)
    menu_dia.delete()
    return HttpResponseRedirect(request.GET['next'])

@login_required    
def menues_normales(request):
    "Abm de los menues para todos los dias"
    error = None
    menu_normal_form = MenuNormalForm()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        contenido = request.POST['contenido']
        if nombre and contenido:
            menu_normal = MenuNormal()
            menu_normal.nombre = nombre
            menu_normal.contenido = contenido
            menu_normal.save()
        else:
            menu_normal_form = MenuNormalForm(request.POST)
            error = "Che, faltan completar algunas cosas."
            
    menues_normales = MenuNormal.objects.all().order_by('nombre')
    return render_to_response('wozoapp/menues_normales.html', {'menues_normales': menues_normales,
                                                               'menu_normal_form': menu_normal_form,
                                                               'user': request.user,
                                                               'root_url': root_url,
                                                               'error': error})

@login_required
def eliminar_menu_normal(request, menu_normal_id):
    "Elimina un menu normal"
    menu_normal = get_object_or_404(MenuNormal, pk=menu_normal_id)
    menu_normal.delete()
    return HttpResponseRedirect(root_url + "menues_normales")
    
def login(request):
    "Inicio de sesion"
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(username=username, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            return HttpResponseRedirect(root_url)
        else:
            error = "Nop, creo que le erraste."

    return render_to_response('wozoapp/login.html', {'user': request.user,
                                                     'root_url': root_url,
                                                     'login_form': LoginForm(),
                                                     'error': error})

def logout(request):
    "Cerrar sesion"
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(root_url + "login")
