from db.py_gihre_db import insertar_asignacion, obtener_trabajadores, obtener_asignaciones_dia, obtener_claves, \
    obtener_graficos
from utils import calcular_rango_anual


def generar_turnos_manual(anho):
    """Genera y asigna turnos manualmente para el año según el gráfico general, evitando duplicados."""

    # Obtenemos el rango de días del año
    primer_dia, ultimo_dia = calcular_rango_anual(anho)

    # Obtener todos los trabajadores, claves y gráficos
    trabajadores = obtener_trabajadores()  # Obtiene todos los trabajadores
    claves = obtener_claves()  # Obtiene todas las claves (turnos)
    graficos = obtener_graficos()  # Obtiene todos los gráficos de turnos de los trabajadores

    for dia in range(primer_dia, ultimo_dia + 1):
        for trabajador in trabajadores:
            id_grafico = trabajador.grafico  # Gráfico asociado al trabajador
            grupo = trabajador.grupo  # Grupo al que pertenece el trabajador

            # Comprobar si existen gráficos y si el trabajador tiene un gráfico asignado
            if graficos:
                grafico = next((g for g in graficos if g.nombre == id_grafico), None)  # Buscar gráfico por nombre

                if grafico:
                    # Convertir los turnos del gráfico en una tupla de enteros
                    ids_claves = tuple(map(int, grafico.turnos.strip('[]').split(',')))

                    # Calcular la clave correspondiente al día actual y el grupo
                    clave = ids_claves[(dia + grupo - 1) % len(ids_claves)]  # La clave correspondiente al turno

                    # Insertar la asignación en la base de datos
                    insertar_asignacion(dia, trabajador.id, clave)
                else:
                    print(
                        f"Advertencia: El trabajador {trabajador.nombre} tiene un gráfico no encontrado: {id_grafico}")
            else:
                print("Advertencia: No hay gráficos disponibles.")


if __name__ == "__main__":
    generar_turnos_manual(2025)