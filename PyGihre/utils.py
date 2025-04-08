import calendar
import configparser


def calcular_rango_dias(mes, anio):
    import calendar
    dias_por_mes = [31, 28 + (1 if calendar.isleap(anio) else 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    inicio = sum(dias_por_mes[:mes - 1]) + 1
    fin = inicio + dias_por_mes[mes - 1] - 1
    return inicio, fin


def calcular_rango_anual(anho):
    """Calcula el rango de días en la base de datos para un año completo."""
    primer_dia = 1
    ultimo_dia = sum(calendar.monthrange(anho, mes)[1] for mes in range(1, 13))
    return primer_dia, ultimo_dia


def convertir_dia_natural_a_bd(dia, mes, anho):
    """Convierte un día natural del mes a su correspondiente en la base de datos."""
    primer_dia_mes = sum(calendar.monthrange(anho, m)[1] for m in range(1, mes))
    return primer_dia_mes + dia


def modo_debug():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.getboolean("general", "debug", fallback=False)