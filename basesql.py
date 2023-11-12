import sqlite3


class Base:
    def abrir(self):
        conexion = sqlite3.connect("base.db")
        return conexion

    def alta(self, datos):
        conn = self.abrir()
        cursor = conn.cursor()

        bandera = False

        cursor.execute("""SELECT id_cliente FROM Cliente WHERE correo = ? """, (datos[1], ))
        resultado = cursor.fetchone()

        if resultado:
            bandera = True
            return (resultado[0], bandera)

        cursor.execute("""INSERT INTO Cliente (nombre, correo, fecha_registro) VALUES (?, ?, ?)""", datos)

        id_cliente = cursor.lastrowid
        
        conn.commit()
        conn.close()

        return (id_cliente, bandera)

    def consulta(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(""" SELECT nombre, correo FROM Cliente where id_cliente = ? """, datos)
            return cursor.fetchall()
        finally:
            conn.close()

    def recuperar_clientes(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute("""SELECT id_cliente, nombre, correo FROM Cliente""")
            return cursor.fetchall()
        finally:
            conn.close()
