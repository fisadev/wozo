from wozo.wozoapp.models import MenuNormal, MenuDia, Pedido
from django.contrib import admin

class MenuNormalAdmin(admin.ModelAdmin):
    fields = ['nombre', 'contenido']
    
    list_display = ('nombre',)

    search_fields = ['nombre', 'contenido']

class MenuDiaAdmin(admin.ModelAdmin):
    fields = ['dia', 'nombre', 'contenido']
    
    list_display = ('dia', 'nombre')

    search_fields = ['nombre', 'contenido']

class PedidoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['dia', 'user']}),
        ("Menu", {'fields': ['menu_normal', 'menu_dia', 'menu_especial']})
    ]
    
    list_display = ('user', 'dia')
    
    list_filter = ['dia']
  

    
admin.site.register(MenuNormal, MenuNormalAdmin)
admin.site.register(MenuDia, MenuDiaAdmin)
admin.site.register(Pedido, PedidoAdmin)
