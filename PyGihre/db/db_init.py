from db.db_setup import engine
from db.models import Base
from py_gihre_db import (
    vaciar_todas_las_tablas,
    insertar_trabajador,
    insertar_clave,
    insertar_grafico
)


def inicializar_datos():
    vaciar_todas_las_tablas()

    # Insertar trabajadores
    insertar_trabajador("Carlos", 1, "A")
    insertar_trabajador("Diego", 4, "A")
    insertar_trabajador("Dani", 8, "B")
    insertar_trabajador("Chamorro", 8, "B")
    insertar_trabajador("MarioB", 7, "B")
    insertar_trabajador("MarioC", 2, "B")
    insertar_trabajador("Dario", 7, "B")
    insertar_trabajador("Minerva", 3, "B")
    insertar_trabajador("Noelia", 6, "B")
    insertar_trabajador("Sergio", 6, "B")
    insertar_trabajador("Luis", 5, "B")
    insertar_trabajador("Alex", 2, "B")

    # Insertar claves
    insertar_clave(1, "T", "5:15", "11:30")
    insertar_clave(2, "T", "15:30", "21:30")

    insertar_clave(3, "T:D4", "20:45", "00:00")
    insertar_clave(4, "T:A3", "00:00", "08:00")
    insertar_clave(5, "T", "07:30", "12:00")
    insertar_clave(6, "T", "10:00", "17:00")

    insertar_clave(10, "R", "05:15", "11:30")
    insertar_clave(11, "R", "14:15", "21:15")

    insertar_clave(99, "D", "0", "0")
    insertar_clave(0, "D", "0", "0")

    # Insertar gráficos
    insertar_grafico("A", "[2,2,2,2,10,0,0,0,10,1,1,1,1,0,0,0]")
    insertar_grafico("B", "[2,3,4,5,6,0,0,0,3,4,5,6,1,0,0,0,3,4,5,6,10,0,0,0]")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    inicializar_datos()
    print("Base de datos inicializada con datos de ejemplo.")