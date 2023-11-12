import sqlite3


class Base:
    def abrir(self):
        conexion = sqlite3.connect("base.db")
        return conexion

    def alta(self, datos):
        conn = self.abrir()
        cursor = conn.cursor()

        bandera = False

        cursor.execute("""SELECT correo FROM Cliente WHERE correo = ?""", (datos[1],))
        resultado = cursor.fetchone()

        if resultado:
            bandera = True
            return (resultado[0], bandera)

        cursor.execute("""INSERT INTO Cliente (nombre, correo, fecha_registro) VALUES (?, ?, ?)""", datos)

        correo = cursor.lastrowid
        
        conn.commit()
        conn.close()

        return (correo, bandera)