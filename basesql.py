import sqlite3
from datetime import datetime, timedelta


class Base:
    def __init__(self):
        self.crear_tablas()
        self.agregar_servicios("Neflix", 7)
        self.agregar_servicios("Disney+", 8)
        self.agregar_servicios("HBO", 10)
        self.agregar_servicios("Star+", 11)

    def abrir(self):
        conn = None
        try:
            conn = sqlite3.connect("base.db")
        except Error as e:
            print(e)

        if conn:
            return conn

    def crear_tablas(self):
        conn = self.abrir()

        try:
            sql = """CREATE TABLE IF NOT EXISTS Cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                correo TEXT,
                fecha_registro DATE
                );"""
            conn.execute(sql)
        except Error as e:
            print(e)
        try:
            sql = """CREATE TABLE IF NOT EXISTS Servicios (
                    id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_plataforma TEXT,
                    precio REAL
                    );"""
            conn.execute(sql)
        except Error as e:
            print(e)
        try:
            sql = """CREATE TABLE IF NOT EXISTS Pantallas (
                    id_pantalla INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER,
                    id_servicio INTEGER,
                    usuario TEXT,
                    contraseña TEXT,
                    correo TEXT,
                    fecha_renovacion DATE,
                    suspendida INTEGER,
                    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE CASCADE,
                    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio) ON DELETE CASCADE
                    );"""
            conn.execute(sql)
        except Error as e:
            print(e)

        try:
            conn.execute(""" PRAGMA foreign_keys=on; """)
        except Error as e:
            print(e)

    def verificar_servicio(self, cursor, nombre):
        cursor.execute(
            """ SELECT COUNT(*) FROM Servicios WHERE nombre_plataforma = ? """,
            (nombre,),
        )
        resultado = cursor.fetchone()
        return resultado[0] > 0

    def agregar_servicios(self, nombre, precio):
        conn = self.abrir()
        cursor = conn.cursor()

        if not self.verificar_servicio(cursor, nombre):
            cursor.execute(
                "INSERT INTO Servicios (nombre_plataforma, precio) VALUES (?, ?)",
                (nombre, precio),
            )
            conn.commit()

    def alta(self, datos):
        conn = self.abrir()
        cursor = conn.cursor()

        bandera = False

        cursor.execute(
            """SELECT id_cliente FROM Cliente WHERE correo = ? """, (datos[1],)
        )
        resultado = cursor.fetchone()

        if resultado:
            bandera = True
            return (resultado[0], bandera)

        cursor.execute(
            """INSERT INTO Cliente (nombre, correo, fecha_registro) VALUES (?, ?, ?)""",
            datos,
        )

        id_cliente = cursor.lastrowid

        conn.commit()
        conn.close()

        return (id_cliente, bandera)

    def consulta(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ SELECT nombre, correo FROM Cliente where id_cliente = ? """, datos
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def modifica_cliente(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ UPDATE Cliente SET nombre = ?, correo = ? WHERE id_cliente = ? """,
                datos,
            )
            conn.commit()
            if cursor.rowcount == 1:
                return f"Se modificó al cliente con id: {datos[2]}"
            else:
                return f"No se pudo modificar al cliente con id: {datos[2]}"
        finally:
            conn.close()

    def elimina_cliente(self, datos):
        conn = self.abrir()
        cursor = conn.cursor()
        cursor.execute("""PRAGMA foreign_keys = ON""")
        cursor.execute(""" DELETE FROM Cliente WHERE id_cliente = ? """, datos)
        conn.commit()
        conn.close()
        if cursor.rowcount > 0:
            return "El cliente ha sido eliminado"
        else:
            return "No se pudo eliminar al cliente"

    def modifica_plataforma(self, datos):
        if datos[0] < 0.0:
            precio = 0
        else:
            precio = datos[0]
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ UPDATE Servicios SET precio = ? WHERE id_servicio = ? """,
                (precio, datos[1]),
            )
            conn.commit()
            return cursor.rowcount
        except:
            conn.close()

    def recuperar_clientes(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute("""SELECT id_cliente, nombre, correo FROM Cliente""")
            return cursor.fetchall()
        finally:
            conn.close()

    def recuperar_plataformas(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ SELECT id_servicio, nombre_plataforma, precio FROM Servicios """
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def agrega_pantalla(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()

            cursor.execute(
                """ SELECT * FROM Cliente WHERE id_cliente = ?""", (datos[0])
            )
            resultado = cursor.fetchone()
            if not resultado:
                return "No existe un usuario con esa id o fue eliminado"

            cursor.execute(
                """ SELECT * FROM Servicios WHERE id_servicio = ? """, (datos[1],)
            )
            resultado = cursor.fetchone()
            if not resultado:
                return "No existe un Servicio con esa id o fue eliminado"

            if len(datos[2]) == 0 or len(datos[3]) == 0 or len(datos[4]) == 0:
                return "No pueden ver campos vacios"

            cursor.execute(
                """ SELECT * FROM Pantallas WHERE usuario = ? """, (datos[2],)
            )
            resultado = cursor.fetchone()
            if resultado:
                return "Ya existe una pantalla que tiene asiganda dicho usuario"

            fecha_hoy = datetime.today()
            suspendida = 0
            if fecha_hoy > datetime.strptime(datos[5], "%m/%d/%y"):
                suspendida = 1

            cursor.execute(
                """ INSERT INTO Pantallas (id_cliente, id_servicio, usuario, contraseña, correo,  fecha_renovacion, suspendida) 
                VALUES (?, ?, ?, ?, ?, ?, ?) """,
                (datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], suspendida),
            )

            id_pantalla = cursor.lastrowid

            conn.commit()
            return f"Pantalla agregada con éxito{id_pantalla}"
        finally:
            conn.close()

    def recuperar_pantallas(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ SELECT id_pantalla, id_cliente, id_servicio, usuario, contraseña, correo, fecha_renovacion, suspendida FROM Pantallas WHERE id_cliente = ?""",
                datos,
            )
            pantallas = cursor.fetchall()

            total = 0
            for pantalla in pantallas:
                cursor.execute(""" SELECT precio FROM Servicios WHERE id_servicio = ? """, (pantalla[2], ))
                precio = cursor.fetchall()
                total += precio[0][0]

            return (pantallas, total)
        finally:
            conn.close()

    def recuperar_vencidos(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM Pantallas""")
            pantallas = cursor.fetchall()

            fecha_hoy = datetime.today()

            for pantalla in pantallas:
                fecha_renovacion = datetime.strptime(pantalla[6], "%m/%d/%y")
                if fecha_hoy > fecha_renovacion:
                    cursor.execute(
                        """ UPDATE Pantallas SET suspendida = 1 WHERE id_pantalla = ? """,
                        (pantalla[0],),
                    )
                else:
                    cursor.execute(
                        """ UPDATE Pantallas SET suspendida = 0 WHERE id_pantalla = ? """,
                        (pantalla[0],),
                    )

            conn.commit()
            cursor.execute(""" SELECT * FROM Pantallas WHERE suspendida = 1""")
            return cursor.fetchall()

        finally:
            conn.close()

    def mostrar_todas_pantallas(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM Pantallas""")
            return cursor.fetchall()

        finally:
            conn.close()

    def consultar_pantalla(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM Pantallas WHERE id_pantalla = ? """,
                datos
            )
            pantalla = cursor.fetchall()
            if pantalla == []:
                return (pantalla, "No hay ninguna pantalla con esa ID")
            else:
                cursor.execute(""" SELECT precio FROM Servicios WHERE id_servicio = ? """, (pantalla[0][2], ))
                precio = cursor.fetchall()
                return (pantalla, f"la pantalla con id {pantalla[0][0]} tiene un precio de {precio[0][0]}$")
        finally:
            conn.close()

    def renovar_pantalla(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM Pantallas WHERE id_pantalla = ? """,
                datos
            )
            pantalla = cursor.fetchall()
            if pantalla == []:
                return "No hay ninguna pantalla con esa ID"
            fecha_hoy = datetime.today()
            fecha_renovacion = datetime.strptime(pantalla[0][6], "%m/%d/%y")
            if fecha_hoy > fecha_renovacion:
                fecha_renovacion +=  timedelta(days=30)
                fecha_renovacion = fecha_renovacion.strftime("%m/%d/%y")
                cursor.execute(
                        """ UPDATE Pantallas SET suspendida = 0, fecha_renovacion = ?  WHERE id_pantalla = ? """,
                        (fecha_renovacion, pantalla[0][0]),
                    )
                conn.commit()
                cursor.execute(""" SELECT * FROM Servicios WHERE id_servicio = ?""",
                    (pantalla[0][2], )
                    )
                servicio = cursor.fetchall()
                costo = servicio[0][2]
                return f"pantalla renovada, se debe pagar {costo}$ y su nueva fecha es para el {fecha_renovacion}" 
            else:
                return "No es necesario renovar la pantalla"

        finally:
            conn.close()

    def eliminar_pantalla(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM Pantallas WHERE id_pantalla = ?""", 
                datos
            )
            pantalla = cursor.fetchall()
            if pantalla == []:
                return "No hay ninguna pantalla con esa ID"
            
            cursor.execute(""" DELETE FROM Pantallas WHERE id_pantalla = ? """, 
                datos
            )
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                return f"La pantalla con ID {datos} ha sido eliminado"
            else:
                return f"No se pudo eliminar la pantalla con ID {datos}"
        
        finally:
            conn.close()
