# Conceptos básicos: #

La aplicación plantea el uso de 3 tipos diferentes de menúes:

  * **Menú Diario**: menúes que se encuentran disponibles en una fecha en particular.
  * **Menú Normal**: menúes que se encuentran siempre disponibles, que pueden pedirse cualquier día.
  * **Menú Especial**: un pedido de algo que no se encuentra listado ni en el Menú Normal ni en el Diario.

Los usuarios podrán pedir lo que cada día deseen como menú, y la aplicación permitirá además realizar un resumen de todo lo pedido para un día particular (este resumen puede ser utilizado para enviarse a quien se compre la comida).

# Implementación: #

La aplicación presenta las siguientes secciones:

## Principal: ##

En esta sección el usuario ve un calendario de la semana actual y la próxima semana. En cada día, se listan los menúes que el usuario pidió y se da la opción de agregar más menúes.
Se pueden eliminar los menúes cargados individualmente.
Cada día se muestra de un color especial dependiendo del estado:
  * **Gris**: normal, sin nada que destacar.
  * **Amarillo**: día futuro en el que todavía no se ha pedido el menú.
  * **Rojo**: día de hoy, cuando no se ha pedido menú para hoy.
  * **Verde**: día de hoy, cuando se ha pedido menú para hoy.
El usuario solo puede modificar (agregar o eliminar) menúes de hoy o de los días posteriores a hoy. No se pueden realizar modificaciones sobre días pasados.

## Resumen: ##

En esta sección el usuario puede seleccionar un día, y la aplicación presenta un resumen de lo que todos los usuarios han pedido para ese día.
Se listan además los usuarios que no han realizado pedidos para el día elegido, con el fin de advertir sobre una posible compra incompleta de menúes.

## Menú Diario: ##

Muy similar a la página principal, aquí se muestran los menúes disponibles para cada día.
Presenta el mismo esquema de calendario y colores que la página principal, pero haciendo referencia a la carga de menúes para cada día.
Los menúes cargados para cada día serán los que se muestren a los usuarios cuando elaboren sus pedidos, como Menúes Diarios.

## Menú Normal: ##

Desde esta sección se cargan los menúes que se encuentran siempre disponibles. Pueden darse de alta o eliminarse.

## Administración: ##

Lleva al sitio de administración de Django.