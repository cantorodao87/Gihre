from db.py_gihre_db import insertar_asignacion, obtener_trabajadores, obtener_claves, \
    obtener_graficos, obtener_asignacion, actualizar_asignacion, obtener_asignaciones_dia
from utils import calcular_rango_anual, modo_debug, log_turno_asignado, log_turno_modificado


def cubrir_turnos_descubiertos_con_reservas(anho):
    claves = obtener_claves()
    claves_trabajo = [c for c in claves if c.tipo.startswith("T")]

    # Obtenemos el rango de días del año
    primer_dia, ultimo_dia = calcular_rango_anual(anho)

    if modo_debug():
        ultimo_dia = 31  # Solo enero en modo debug

    for dia in range(primer_dia, ultimo_dia + 1):
        asignaciones = obtener_asignaciones_dia(dia)
        asignadas_ids = {a.clave.id for a in asignaciones}
        no_asignadas = [c for c in claves_trabajo if c.id not in asignadas_ids]

        reservas = [a for a in asignaciones if a.clave.tipo == "R"]
        for clave_descubierta in no_asignadas:
            if reservas:
                reserva = reservas.pop(0)
                actualizar_asignacion(dia, reserva.trabajador_id, clave_descubierta.id)
                log_turno_modificado(dia, reserva.trabajador_id, reserva.clave_id, clave_descubierta.id)


def obtener_clave(dia, trabajador, grafico, claves, asignaciones_existentes):
    """
    Determina la clave de turno para un trabajador en un día concreto, aplicando lógica de rotación,
    y reglas para evitar claves duplicadas y validar claves anexas (T:A?).

    :param dia: Día del año (int)
    :param trabajador: trabajador (model)
    :param grafico: grafico del trabajador (model)
    :param claves: todas las claves
    :param asignaciones_existentes: set[(dia, clave_id)] ya insertadas
    :return: ID de la clave a asignar
    """

    claves_dict = {clave.id: clave for clave in claves}

    # Convertir los turnos del gráfico en una tupla de enteros
    ids_claves = tuple(map(int, grafico.turnos.strip('[]').split(',')))

    # Rotación: cada trabajador comienza desde su grupo
    indice = (dia + trabajador.grupo - 1) % len(ids_claves)

    clave_id = ids_claves[indice]
    clave = claves_dict.get(clave_id)

    if not clave:
        print(f"Clave {clave_id} no encontrada en claves_dict.")
        return 10  # reserva por defecto

    # Si es una clave de trabajo, comprobamos
    if clave.tipo.startswith("T"):

        # Claves que dependen de otras, hacemos la comprobacion con el día previo
        if clave.tipo.startswith("T:A"):
            id_clave_anterior = int(clave.tipo.split("A")[1])
            asignacion_dia_anterior = obtener_asignacion(dia-1, trabajador.id)
            if id_clave_anterior == asignacion_dia_anterior:
                return clave_id
            else:
                return 10

        # Si ya tiene asignación para este día, usamos una reserva
        if (dia, clave_id) in asignaciones_existentes:
            return 10
        else:
            return clave_id

    # Claves que no son de trabajo, por ejemplo vacaciones o descansos, se asignan directamente
    else:
        return clave.id


def generar_turnos(anho):
    """Genera y asigna turnos manualmente para el año según el gráfico general, evitando duplicados."""

    # Obtenemos el rango de días del año
    primer_dia, ultimo_dia = calcular_rango_anual(anho)

    if modo_debug():
        ultimo_dia = 31  # Solo enero en modo debug

    # Obtener todos los trabajadores, claves y gráficos
    trabajadores = obtener_trabajadores()  # Obtiene todos los trabajadores
    claves = obtener_claves()  # Obtiene todas las claves (turnos)
    graficos = obtener_graficos()  # Obtiene todos los gráficos de turnos de los trabajadores

    for dia in range(primer_dia, ultimo_dia + 1):

        asignaciones_existentes = set()

        #TODO Recorrer trabajadores con órdenes alternativos
        for trabajador in trabajadores:
            id_grafico = trabajador.grafico  # Gráfico asociado al trabajador

            # Comprobar si existen gráficos y si el trabajador tiene un gráfico asignado
            if graficos:
                grafico = next((g for g in graficos if g.nombre == id_grafico), None)  # Buscar gráfico por nombre

                if grafico:

                    clave_id = obtener_clave(
                        dia,
                        trabajador,
                        grafico,
                        claves,
                        asignaciones_existentes
                    )

                    insertar_asignacion(dia, trabajador.id, clave_id)

                    log_turno_asignado(dia, trabajador.nombre, clave_id)
                    asignaciones_existentes.add((dia, clave_id))

                else:
                    print(
                        f"Advertencia: El trabajador {trabajador.nombre} tiene un gráfico no encontrado: {id_grafico}")
            else:
                print("Advertencia: No hay gráficos disponibles.")

    # Nueva pasada para cubrir turnos descubiertos con reservas
    cubrir_turnos_descubiertos_con_reservas(anho)


if __name__ == "__main__":
    generar_turnos(2025)