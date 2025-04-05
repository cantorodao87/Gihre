from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.orm import joinedload

from db.db_setup import SessionLocal
from db.models import Trabajador, Clave, Asignacion, Grafico

def vaciar_todas_las_tablas():
    with SessionLocal() as session:
        # El orden importa por las relaciones (FKs)
        session.execute(delete(Asignacion))
        session.execute(delete(Trabajador))
        session.execute(delete(Clave))
        session.execute(delete(Grafico))
        session.commit()

def obtener_trabajadores():
    with SessionLocal() as session:
        return session.query(Trabajador).all()

def obtener_claves():
    with SessionLocal() as session:
        return session.query(Clave).all()

def obtener_asignaciones():
    with SessionLocal() as session:
        return session.query(Asignacion).all()

def obtener_graficos():
    with SessionLocal() as session:
        return session.query(Grafico).all()

def obtener_asignaciones_dia(dia: int):
    with SessionLocal() as session:
        asignaciones = (
            session.query(Asignacion)
            .filter(Asignacion.dia == dia)
            .options(joinedload(Asignacion.clave))
            .all()
        )
    return asignaciones

def insertar_asignacion(dia: int, trabajador_id: int, clave_id: int):
    with SessionLocal() as session:
        nueva = Asignacion(dia=dia, trabajador_id=trabajador_id, clave_id=clave_id)
        session.add(nueva)
        session.commit()

def obtener_grafico_por_nombre(nombre: str):
    with SessionLocal() as session:
        return session.query(Grafico).filter_by(nombre=nombre).first()

def insertar_grafico(nombre: str, turnos: str):
    with SessionLocal() as session:
        nuevo = Grafico(nombre=nombre, turnos=turnos)
        session.add(nuevo)
        session.commit()

def insertar_trabajador(nombre: str, grupo: int, grafico: str = None):
    with SessionLocal() as session:
        nuevo = Trabajador(nombre=nombre, grupo=grupo, grafico=grafico)
        session.add(nuevo)
        session.commit()

def insertar_clave(id_clave: int, tipo: str, hora_comienzo: str, hora_final: str):
    with SessionLocal() as session:
        nueva = Clave(id=id_clave, tipo=tipo, hora_comienzo=hora_comienzo, hora_final=hora_final)
        session.add(nueva)
        session.commit()


def obtener_turnos_mes(mes: int, ano: int):
    """
    Obtiene los turnos de los trabajadores para un mes y año específicos.

    Parámetros:
    db: La sesión de la base de datos.
    mes: El mes del que se quieren obtener los turnos (1-12).
    ano: El año del que se quieren obtener los turnos.

    Retorna:
    Una lista de diccionarios con los datos de los turnos.
    """
    with SessionLocal() as session:
        # Fecha de inicio y fin del mes
        primer_dia = datetime.date(ano, mes, 1)
        if mes == 12:
            ultimo_dia = datetime.date(ano + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            ultimo_dia = datetime.date(ano, mes + 1, 1) - datetime.timedelta(days=1)

        # Consulta para obtener las asignaciones dentro del rango de fechas
        asignaciones = session.query(Asignacion, Trabajador, Clave) \
            .join(Trabajador, Trabajador.id == Asignacion.trabajador_id) \
            .join(Clave, Clave.id == Asignacion.clave_id) \
            .filter(Asignacion.dia >= primer_dia.day) \
            .filter(Asignacion.dia <= ultimo_dia.day) \
            .all()

        # Procesar los resultados y agruparlos por trabajador
        turnos_mes = {}

        for asignacion, trabajador, clave in asignaciones:
            trabajador_nombre = trabajador.nombre
            turno = {
                "tipo": clave.tipo,
                "hora_comienzo": clave.hora_comienzo,
                "hora_final": clave.hora_final,
                "dia": asignacion.dia
            }

            if trabajador_nombre not in turnos_mes:
                turnos_mes[trabajador_nombre] = []

            turnos_mes[trabajador_nombre].append(turno)

    return turnos_mes