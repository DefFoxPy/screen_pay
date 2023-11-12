from tkinter import *
import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("streaming_service.db")

# Crear un cursor
c = conn.cursor()

# Crear tabla de clientes
c.execute(
    """
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    correo TEXT UNIQUE
)
"""
)

# Crear tabla de plataformas
c.execute(
    """
CREATE TABLE plataformas (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE
)
"""
)

# Crear tabla de cuentas
c.execute(
    """
CREATE TABLE cuentas (
    id INTEGER PRIMARY KEY,
    usuario TEXT,
    contraseña TEXT,
    id_cliente INTEGER,
    id_plataforma INTEGER,
    num_pantallas INTEGER,
    fecha_renovacion TEXT,
    monto_total REAL,
    FOREIGN KEY (id_cliente) REFERENCES clientes (id),
    FOREIGN KEY (id_plataforma) REFERENCES plataformas (id)
)
"""
)

# Guardar los cambios
conn.commit()

# Cerrar la conexión
conn.close()


# Función para insertar un cliente
def insertar_cliente():
    # Conectar a la base de datos
    conn = sqlite3.connect("streaming_service.db")
    c = conn.cursor()

    # Insertar un cliente
    c.execute(
        """
    INSERT INTO clientes (nombre, correo)
    VALUES (?, ?)
    """,
        (entry_nombre.get(), entry_correo.get()),
    )

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    # Limpiar los campos de entrada
    entry_nombre.delete(0, END)
    entry_correo.delete(0, END)


# Crear la ventana de Tkinter
root = Tk()

# Crear campos de entrada para el nombre y el correo
entry_nombre = Entry(root)
entry_nombre.pack()
entry_correo = Entry(root)
entry_correo.pack()

# Crear un botón para insertar el cliente
button_insertar = Button(root, text="Insertar cliente", command=insertar_cliente)
button_insertar.pack()

# Iniciar el bucle principal de Tkinter
root.mainloop()
