import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import ttk

from db.py_gihre_db import obtener_trabajadores, obtener_asignaciones_dia
from utils import calcular_rango_anual  # Para obtener el rango de días del año


def obtener_turnos_por_mes(mes, anho):
    """Obtiene las asignaciones de turnos para el mes y año seleccionados, con el día transformado a día del año."""
    primer_dia, ultimo_dia = calcular_rango_anual(anho)

    # Para cada día del mes, calculamos el número de día del año
    asignaciones = {}
    for dia_mes in range(1, 32):
        if dia_mes > ultimo_dia:  # Si el día del mes excede el último día del año, paramos
            break
        # Convertimos el día del mes a un número de día del año
        dia_del_anho = primer_dia + dia_mes - 1
        asignaciones[dia_mes] = obtener_asignaciones_dia(dia_del_anho)  # Asignación para el día específico

    return asignaciones


def generar_tabla():
    """Genera la tabla de turnos para los trabajadores en función del mes seleccionado."""
    mes = mes_combobox.get()  # Obtenemos el mes seleccionado
    anho = 2025  # Podemos añadir un selector para el año más tarde
    asignaciones = obtener_turnos_por_mes(mes, anho)

    # Limpiar la tabla existente
    for row in tabla.get_children():
        tabla.delete(row)

    # Insertar las filas (trabajadores)
    for trabajador in trabajadores:
        # Insertar el trabajador en la primera columna
        fila = [trabajador.nombre]

        # Obtener las asignaciones de este trabajador
        for dia in range(1, 32):  # Aquí podemos ajustar dependiendo de los días del mes
            id_asignacion = None
            # Buscar la asignación de este trabajador para este día
            for asignacion in asignaciones.get(dia, []):
                if asignacion.trabajador_id == trabajador.id:  # Comprobamos si la asignación corresponde a este trabajador
                    id_asignacion = asignacion.clave.id
                    break
            fila.append(id_asignacion if id_asignacion else "-")  # Añadir la asignación o un guión si no existe

        tabla.insert("", "end", values=fila)


def on_item_click(event):
    """Función para editar la celda seleccionada."""
    item = tabla.selection()[0]  # Obtener el item seleccionado
    col = tabla.identify_column(event.x)  # Identificar la columna donde se hace clic
    col = int(col.strip('#')) - 1  # Convertir a índice de columna

    # Si es una columna válida, permitir editar
    if col > 0:  # Evitar que se edite la columna de trabajadores
        old_value = tabla.item(item, "values")[col]
        new_value = tk.simpledialog.askstring("Editar turno", f"Nuevo valor para el día {col}:", initialvalue=old_value)
        if new_value:
            tabla.item(item, values=tuple(new_value if i == col else tabla.item(item, "values")[i] for i in range(len(tabla["columns"]))))


# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Turnos")

# Configuración de la cuadrícula
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Selección de mes
mes_label = tk.Label(root, text="Selecciona el mes:")
mes_label.grid(row=0, column=0, padx=10, pady=5)

mes_combobox = ttk.Combobox(root, values=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                                          "Septiembre", "Octubre", "Noviembre", "Diciembre"])
mes_combobox.grid(row=0, column=1, padx=10, pady=5)
mes_combobox.set("Enero")  # Establecer un valor predeterminado

# Botón para generar la tabla
generar_button = tk.Button(root, text="Generar Tabla", command=generar_tabla)
generar_button.grid(row=0, column=2, padx=10, pady=5)

# Tabla para mostrar los turnos
tabla = ttk.Treeview(root, columns=["Trabajador"] + [str(i) for i in range(1, 32)], show="headings", height=15)
tabla.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Configurar encabezados y tamaños de columnas
tabla.heading("#1", text="Trabajador")
for i in range(1, 32):
    tabla.heading(f"{i}", text=f"{i}")  # Mostrar solo el número del día
    tabla.column(f"{i}", width=30, anchor="center", stretch=tk.NO)  # Establecer el ancho de las columnas

# Asociar evento de clic en las celdas
tabla.bind("<ButtonRelease-1>", on_item_click)

# Obtener los trabajadores de la base de datos
trabajadores = obtener_trabajadores()

# Iniciar la interfaz gráfica
root.mainloop()