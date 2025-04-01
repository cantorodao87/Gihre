import py_gihre_db


def inicializar_datos():
    py_gihre_db.init_db()

    py_gihre_db.vaciar_todas_las_tablas()

    # Insertar trabajadores
    py_gihre_db.insertar_trabajador("Carlos", 1, "[A]")
    py_gihre_db.insertar_trabajador("Diego", 4, "[A]")
    py_gihre_db.insertar_trabajador("Dani", 8, "[A, B]")
    py_gihre_db.insertar_trabajador("Chamorro", 8, "[A, B]")
    py_gihre_db.insertar_trabajador("MarioB", 7, "[A, B]")
    py_gihre_db.insertar_trabajador("MarioC", 2, "[A, B]")
    py_gihre_db.insertar_trabajador("Dario", 7, "[A, B]")
    py_gihre_db.insertar_trabajador("Minerva", 3, "[A, B]")
    py_gihre_db.insertar_trabajador("Noelia", 6, "[A, B]")
    py_gihre_db.insertar_trabajador("Sergio", 6, "[A, B]")
    py_gihre_db.insertar_trabajador("Luis", 5, "[A, B]")
    py_gihre_db.insertar_trabajador("Alex", 2, "[A, B]")

    # Insertar turnos
    py_gihre_db.insertar_clave(1,"5:15", "11:30")
    py_gihre_db.insertar_clave(2, "15:30", "21:30")

    py_gihre_db.insertar_clave(3,"20:45", "00:00")
    py_gihre_db.insertar_clave(4, "00:00", "08:00")
    py_gihre_db.insertar_clave(5, "07:30", "12:00")
    py_gihre_db.insertar_clave(6, "10:00", "17:00")

    py_gihre_db.insertar_clave(10, "05:15", "11:30")
    py_gihre_db.insertar_clave(11, "14:15", "21:15")

    py_gihre_db.insertar_clave(99, "0", "0")
    py_gihre_db.insertar_clave(0, "0", "0")

    # Insertar gráficos
    py_gihre_db.insertar_grafico("A", "[2,2,2,2,2,99,99,99,10,1,1,1,1,99,99,99]")
    py_gihre_db.insertar_grafico("B", "[2,3,4,5,6,99,99,99,3,4,5,6,1,99,99,99]")

    # Insertar asignaciones de turnos
    # py_gihre_db.insertar_asignacion(1, 1, 1)


if __name__ == "__main__":
    inicializar_datos()
    print("Base de datos inicializada con datos de ejemplo.")