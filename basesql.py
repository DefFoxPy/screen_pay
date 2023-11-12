import sqlite3


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
                    pantallas_compradas INTEGER,
                    fecha_renovacion DATE,
                    suspendida INTEGER,
                    FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente),
                    FOREIGN KEY (id_servicio) REFERENCES Servicios (id_servicio)
                    );"""
            conn.execute(sql)
        except Error as e:
            print(e)

    def verificar_servicio(self, cursor, nombre):
        cursor.execute(
            """ SELECT COUNT(*) FROM Servicios WHERE nombre_plataforma = ? """, (nombre, )
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
                """ UPDATE Cliente set nombre = ?, correo = ? where id_cliente = ? """,
                datos,
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
            cursor.execute(""" SELECT id_servicio, nombre_plataforma, precio FROM Servicios """)
            return cursor.fetchall()
        finally:
            conn.close()
