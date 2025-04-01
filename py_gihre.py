from itertools import cycle
import sqlite3
from db.py_gihre_db import insertar_asignacion, obtener_trabajadores

# Definición de constantes
TRABAJADORES = 11
TURNOS = [1, 2, 3, 4, 5, 6, 10]  # El 10 es reserva
DESCANSO = 'D'

# Patrón fijo de Carlos (grupo 1) y Diego (grupo 4)
PATRON_CARLOS = [2, 2, 2, 2, 2, DESCANSO, DESCANSO, DESCANSO, 10, 1, 1, 1, 1, DESCANSO, DESCANSO, DESCANSO]
PATRON_DIEGO = [10, 1, 1, 1, 1, DESCANSO, DESCANSO, DESCANSO, 2, 2, 2, 2, 2, DESCANSO, DESCANSO, DESCANSO]
PATRON_CARLOS *= (365 // len(PATRON_CARLOS)) + 1  # Repetimos hasta cubrir el año
PATRON_DIEGO *= (365 // len(PATRON_DIEGO)) + 1

# Grupos de trabajo
GRUPOS = 8

# Definimos las semanas permitidas
SEMANA_1 = [3, 4, 5, 6, 10]
SEMANA_2 = [10, 3, 4, 5, 6]

# Definir los días de inicio de cada grupo
INICIO_GRUPOS = [0, 1, 2, 3, 4, 5, 6, 7]  # Distribuir inicio de cada grupo


def generar_turnos():
    trabajadores = obtener_trabajadores()

    calendario = [[] for _ in range(TRABAJADORES)]
    ocupacion_diaria = [[] for _ in range(365)]  # Para controlar que no haya turnos duplicados por día

    # Asignamos patrones fijos a Carlos y Diego
    calendario[0] = PATRON_CARLOS[:365]  # Carlos (Grupo 1)
    calendario[3] = PATRON_DIEGO[:365]  # Diego (Grupo 4)

    # Registrar turnos de Carlos y Diego
    for dia, turno in enumerate(calendario[0]):
        if turno != DESCANSO:
            ocupacion_diaria[dia].append(turno)
    for dia, turno in enumerate(calendario[3]):
        if turno != DESCANSO:
            ocupacion_diaria[dia].append(turno)

    # Distribuimos los trabajadores en grupos escalonados con sus descansos
    for i in range(1, TRABAJADORES):
        if i == 3:  # Diego ya asignado
            continue
        grupo = (i - 1) % GRUPOS
        semana_tipo = SEMANA_1 if grupo % 2 == 0 else SEMANA_2

        dia_actual = INICIO_GRUPOS[grupo]  # Cada grupo comienza en un día diferente
        while len(calendario[i]) < 365:
            for turno in semana_tipo:
                if len(calendario[i]) >= 365:
                    break
                dia = dia_actual + len(calendario[i])  # Ajustamos el día real en el año
                if dia >= 365:
                    break
                # Evitamos turnos repetidos en el mismo día
                if turno not in ocupacion_diaria[dia]:
                    calendario[i].append(turno)
                    ocupacion_diaria[dia].append(turno)
                else:
                    calendario[i].append(10)  # Asignamos reserva si está repetido
                    ocupacion_diaria[dia].append(10)

            # Asignamos 3 días de descanso
            for _ in range(3):
                if len(calendario[i]) < 365:
                    calendario[i].append(DESCANSO)

    # Insertar turnos en la base de datos
    for usuario, turnos in zip(trabajadores, calendario):
        for dia, turno in enumerate(turnos):
            if turno != DESCANSO:
                insertar_asignacion(dia, usuario[0], turno)

    return calendario


# Generamos los turnos del año
distribucion = generar_turnos()

# Mostramos un fragmento de los turnos generados
for i, trabajador in enumerate(distribucion):
    print(f"Trabajador {i + 1}: {trabajador[:30]}...")  # Mostramos solo los primeros 30 días
