import sqlite3
import os
import calendar

from utils import calcular_rango_dias

# Obtener la ruta absoluta de la carpeta "db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta "db"
DB_PATH = os.path.join(BASE_DIR, "py_gihre.db")  # Ruta a la base de datos dentro de "db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de trabajadores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabajadores (
        id_trabajador INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        grupo INTEGER NOT NULL,
        graficos TEXT
    )
    ''')

    # Tabla de claves
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS claves (
        id_clave INTEGER PRIMARY KEY,
        hora_comienzo TEXT NOT NULL,
        hora_final TEXT NOT NULL
    )
    ''')

    # Tabla de gráficos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS graficos (
        id_grafico INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_grafico TEXT NOT NULL,
        turnos TEXT NOT NULL
    )
    ''')

    # Tabla de asignación de turnos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS asignaciones (
        id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
        dia INTEGER NOT NULL,
        id_trabajador INTEGER NOT NULL,
        id_clave INTEGER NOT NULL,
        UNIQUE(dia, id_trabajador, id_clave),
        FOREIGN KEY (id_trabajador) REFERENCES trabajadores(id_trabajador),
        FOREIGN KEY (id_clave) REFERENCES claves(id_clave)
    )
    ''')

    conn.commit()
    conn.close()


def select_all(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_all(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    conn.commit()
    conn.close()

def vaciar_todas_las_tablas():
    tablas = ["trabajadores", "claves", "asignaciones", "graficos"]
    for tabla in tablas:
        delete_all(tabla)

def insertar_trabajador(nombre, grupo, graficos):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trabajadores (nombre, grupo, graficos) VALUES (?, ?, ?)", (nombre, grupo, graficos))
    conn.commit()
    conn.close()


def insertar_clave(clave, hora_comienzo, hora_final):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO claves (id_clave, hora_comienzo, hora_final) VALUES (?, ?, ?)",
                   (clave, hora_comienzo, hora_final))
    conn.commit()
    conn.close()

def insertar_asignacion(dia, trabajador_id, clave_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO asignaciones (dia, id_trabajador, id_clave) VALUES (?, ?, ?)",
                   (dia, trabajador_id, clave_id))
    conn.commit()
    conn.close()

def insertar_grafico(nombre_grafico, turnos):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO graficos (nombre_grafico, turnos) VALUES (?, ?)", (nombre_grafico, turnos))
    conn.commit()
    conn.close()


def obtener_trabajadores():
    return select_all("trabajadores")


def obtener_claves():
    return select_all("claves")


def obtener_asignaciones():
    return select_all("asignaciones")


def obtener_graficos():
    return select_all("graficos")


def obtener_turnos_mes(anho, mes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener trabajadores
    cursor.execute("SELECT id_trabajador, nombre FROM trabajadores")
    trabajadores = cursor.fetchall()

    inicio, fin = calcular_rango_dias(mes, anho)

    # Obtener turnos asignados
    cursor.execute("""
    SELECT 
    a.dia, 
    t.nombre AS trabajador,
    t.id_trabajador AS id_trabajador, 
    c.id_clave AS clave
    FROM asignaciones a
    JOIN trabajadores t ON a.id_trabajador = t.id_trabajador
    JOIN claves c ON a.id_clave = c.id_clave
    WHERE a.dia BETWEEN ? AND ? 
    ORDER BY a.dia, t.nombre;
    """, (inicio, fin))

    asignaciones = cursor.fetchall()

    #print(asignaciones)

    conn.close()

    # Crear diccionario de turnos
    turnos_dict = {trabajador[0]: {dia: "" for dia in range(1, calendar.monthrange(anho, mes)[1] + 1)} for trabajador in trabajadores}
    #
    for dia, trabajador, id_trabajador, clave in asignaciones:
         if id_trabajador in turnos_dict:
             turnos_dict[id_trabajador][dia] = clave

    return trabajadores, turnos_dict
