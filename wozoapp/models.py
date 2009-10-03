from django.db import models
from django.contrib.auth.models import User

class MenuNormal(models.Model):
    "Menu que puede ser usado cualquier dia"
    nombre = models.CharField(max_length=50)
    contenido = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.nombre
    
class MenuDia(models.Model):
    "Menu disponible en un dia especifico"
    dia = models.DateField()
    nombre = models.CharField(max_length=50)
    contenido = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.nombre
    
class Pedido(models.Model):
    "Pedido de un menu determinado por parte de un usuario"
    dia = models.DateField()
    user = models.ForeignKey(User)
    menu_normal = models.ForeignKey(MenuNormal, null=True, blank=True)
    menu_dia = models.ForeignKey(MenuDia, null=True, blank=True)
    menu_especial = models.CharField(max_length=250, null=True, blank=True)
    
    def __unicode__(self):
        return str(self.user) + " para el " + str(self.dia)

