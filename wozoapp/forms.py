from django import forms
from models import MenuDia, MenuNormal, Pedido

class LoginForm(forms.Form):
    "Formulario de inicio de sesion"
    username = forms.CharField(max_length=100, label='Usuario:')
    password = forms.CharField(max_length=100, label='Password:',
                               widget=forms.PasswordInput(render_value=False))

class PedidoForm(forms.Form):
    "Formulario de pedido de menu"
    menu_normal = forms.ChoiceField(choices=[])
    menu_dia = forms.ChoiceField(choices=[])
    menu_especial = forms.CharField(max_length=100)

class MenuNormalForm(forms.Form):
    "Formulario de nuevo menu normal"
    nombre = forms.CharField(max_length=50)
    contenido = forms.CharField(max_length=250)

class MenuDiaForm(forms.Form):
    "Formulario de nuevo menu del dia"
    nombre = forms.CharField(max_length=50)
    contenido = forms.CharField(max_length=250)
