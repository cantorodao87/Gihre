from itertools import cycle
import sqlite3
from db.py_gihre_db import insertar_asignacion, obtener_trabajadores, obtener_asignaciones_dia
from utils import calcular_rango_anual

# Definición de constantes
TURNOS = [1, 2, 3, 4, 5, 6, 10]  # El 10 es reserva
DESCANSO = 99

# Gráficos para Diego y Carlos
GRAFICO_CARLOS = [2, 2, 2, 2, 2, DESCANSO, DESCANSO, DESCANSO, 10, 1, 1, 1, 1, DESCANSO, DESCANSO, DESCANSO]
GRAFICO_DIEGO = [10, 1, 1, 1, 1, DESCANSO, DESCANSO, DESCANSO, 2, 2, 2, 2, 2, DESCANSO, DESCANSO, DESCANSO]

# Gráfico general
GRAFICO_GENERAL = [3, 4, 5, 6, 10, DESCANSO, DESCANSO, DESCANSO, 10, 3, 4, 5, 6, DESCANSO, DESCANSO, DESCANSO]

def generar_turnos_manual(anho):
    """Genera y asigna turnos manualmente para todo el año según el gráfico general, evitando duplicados."""
    trabajadores = obtener_trabajadores()
    primer_dia, ultimo_dia = calcular_rango_anual(anho)

    for trabajador in trabajadores:
        id_trabajador = trabajador[0]
        grupo = trabajador[2]
        grafico = GRAFICO_GENERAL
        if id_trabajador == 1:
            grafico = GRAFICO_CARLOS
        elif id_trabajador == 4:
            grafico = GRAFICO_DIEGO

        longitud_grafico = len(grafico)

        for i, dia in enumerate(range(primer_dia, ultimo_dia + 1)):
            turno_asignado = grafico[(i+grupo-1) % longitud_grafico]
            if turno_asignado == DESCANSO:
                None
            else:
                # Comprobar si el turno ya está asignado en la BBDD
                turnos_existentes = obtener_asignaciones_dia(dia)
                # Extraer los turnos de las asignaciones (el 4º elemento de la tupla es el turno)
                turnos_dia = [turno for _, _, _, turno in turnos_existentes]
                if turno_asignado in turnos_dia:
                    turno_asignado = 10  # Reserva si el turno ya existe

            # Insertar la asignación en la base de datos
            insertar_asignacion(dia, id_trabajador, turno_asignado)


if __name__ == "__main__":
    generar_turnos_manual(2025)