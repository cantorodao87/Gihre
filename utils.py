import calendar

def calcular_rango_dias(mes, anio):
    import calendar
    dias_por_mes = [31, 28 + (1 if calendar.isleap(anio) else 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    inicio = sum(dias_por_mes[:mes - 1]) + 1
    fin = inicio + dias_por_mes[mes - 1] - 1
    return inicio, fin