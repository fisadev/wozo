from datetime import date, datetime, timedelta

#dias que no se deben mostrar en las listas (mis pedidos, menues diarios y
#resumen de mpedidos)
#0 a 6 = lunes a domingo de la primer semana
#7 a 13 = lunes a domingo de la segunda semana
DIAS_EXCLUIR = [5, 6, 12, 13]

#url base de la aplicacion, actualizar si se cambia el urls.py del proyecto!
root_url = "/wozo/"

#Descripcion de los dias de la semana
DIAS_SEMANA = ['Lunes',
               'Martes',
               'Miercoles',
               'Jueves',
               'Viernes',
               'Sabado',
               'Domingo']

def obtener_dias():
    """Arma una lista de los dias de esta semana y la siguiente.
    
    Devuelve una lista con el formato:
    numero, fecha, dia_semana, semana
    
    No incluye los dias de DIAS_EXCLUIR.
    
    """
    hoy = date.today()
    #primer dia de esta semana
    primer_dia = hoy - timedelta(days=hoy.weekday())
    
    #armar lista de dias
    return [(i,
             primer_dia + timedelta(days = i),
             DIAS_SEMANA[i % 7],
             ((i < 7) and [0,] or [1,])[0])
            for i in range(14)
            if i not in DIAS_EXCLUIR]
