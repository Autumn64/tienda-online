# Esta es una abstracción de los tipos de consulta en MySQL con base en los procedimientos
# CRUD. Para utilizar la interfaz proporcionada por esta clase se pasan los argumentos
# en forma de diccionario, y se especifican los parámetros que después se insertarán en la
# consulta, los cuales, dependiendo de la consulta concreta, pueden ser los siguientes:
# {
#     "table": "tabla a seleccionar",
#     "columns": ["columnas de la consulta", "separadas en una lista"],
#     "values": ["valores", "separados en una lista"],
#     "conditions": [
#         {
#             "prefix": "prefijo (WHERE, AND, OR, etc)",
#             "operator": "operador de comparación (=, >, <, etc)",
#             "column": "columna que se va a comparar",
#             "value": "valor contra el que se va a comparar"
#         },
#         {
#             "prefix": "(WHERE, AND, OR, etc)",
#             "operator": "(=, >, <, etc)",
#             "column": "cada condición",
#             "value": "se coloca con el mismo formato en la lista"
#         }
#     ]
# }
# Esta abstracción tiene la ventaja de que no es necesario poner las consultas directamente
# en el código ya que basta con utilizar los métodos proporcionados, lo que se traduce en
# código más legible y modificable, además de que se podría adaptar a otros tipos de base de datos 
# (SQL Server, Oracle, PostgreSQL) sin necesidad de reescribir todo el código. Por otra parte, 
# se tiene la desventaja de que la interfaz podría no ser muy flexible, y sería más bien 
# contraproducente para consultas complejas. Mi recomendación personal es que, si se necesitan hacer 
# consultas complejas, conviene más crear una vista desde MySQL que permita obtener esa información 
# mediante una consulta simple.

# Adicionalmente, se proporciona una interfaz `debug_query` que imprime las consultas resultantes,
# para verificar que se estén generando correctamente. Esta herramienta está hecha con fines de
# depuración y NO debe utilizarse en producción.

# No hay que olvidar desconectar la base de datos manualmente con el método `disconnect()`,
# ya que de no hacerlo la conexión se quedaría abierta indefinidamente.

import os, mysql.connector

class Database():
    def __init__(self):
        # `self.db` representa a la conexión en sí, mientras que `self.cursor`
        # representa el objeto que hará las consultas a la base de datos.
        self.db = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASS"),
            database = os.getenv("DB_DATABASE"),
        )

        self.cursor = self.db.cursor(dictionary=True)

    def disconnect(self) -> None:
        self.cursor.close()
        self.db.close()
    
    def parseParameters(self, parameters: list) -> (str, list):
        # Convierte las condiciones pasadas por la interfaz a sintaxis SQL.
        params = ""
        statement = []

        for element in parameters:
            params += f" {element['prefix']} {element['column']} {element['operator']} %s"
            statement.append(element['value'])
        
        return params, statement

    def prepareStatementSelect(self, parameters: dict) -> (str, list):
        # Genera la sintaxis SQL adecuada para una consulta de tipo SELECT. Los parámetros
        # requeridos para este tipo de consultas son `table`, `columns` y opcionalmente `conditions`.
        # Un ejemplo de consulta válida es el siguiente:
        # {
        #     "table": "usuarios",
        #     "columns": ["id", "username", "passwd"],
        #     "conditions": [
        #         {
        #             "prefix": "WHERE",
        #             "operator": "=",
        #             "column": "email",
        #             "value": "ejemplo@correo.com"
        #         },
        #         {
        #             "prefix": "AND",
        #             "operator": "=",
        #             "column": "verificado",
        #             "value": True
        #         },
        #     ]
        # }
        # Lo cual produciría exactamente la siguiente consulta en sintaxis SQL:
        # SELECT id, username, passwd FROM usuarios WHERE email=ejemplo@correo.com AND verificado=TRUE;
        # `statement` representa las variables que se van a procesar en la consulta.

        columns = ", ".join(parameters["columns"])
        table = parameters["table"]

        statement = []
        query: str = f"SELECT {columns} FROM {table}"

        if not "conditions" in parameters:
            return query, statement

        conditions, statement = self.parseParameters(parameters["conditions"])

        query += conditions
        
        return query, statement

    def prepareStatementInsert(self, parameters: dict) -> (str, list):
        # Genera la sintaxis SQL adecuada para una consulta de tipo INSERT. Los parámetros
        # requeridos para este tipo de consultas son `table`, `columns` y `values`.
        # Un ejemplo de inserción válida es el siguiente:
        # {
        #     "table": "tokens",
        #     "columns": ["username_id", "fecha_creacion", "fecha_expiracion"],
        #     "values": [5, "2025-10-11 07:32:55", "2025-11-11 07:32:35"]
        # }
        # Lo cual produciría exactamente la siguiente consulta en sintaxis SQL:
        # INSERT INTO tokens (username_id, fecha_creacion, fecha_expiracion)
        # VALUES (5, 2025-10-11 07:32:55, 2025-11-11 07:32:35);
        # `values` representa las variables que se van a procesar en la consulta.

        if len(parameters["columns"]) != len(parameters["values"]):
            # Si el número de columnas y de valores no coincide, lanza una excepción
            raise Exception("Number of columns and values doesn't coincide")

        columns = "(" + ", ".join(parameters["columns"]) + ")"
        table = parameters["table"]
        values = parameters["values"]

        query: str = f"INSERT INTO {table} {columns} VALUES ("

        for _ in values:
            query +="%s, "
        
        # Elimina el `, ` del final y agrega el último paréntesis.
        query = query[:-2] + ")"

        return query, values
    
    def prepareStatementUpdate(self, parameters: dict) -> (str, list):
        # Genera la sintaxis SQL adecuada para una consulta de tipo UPDATE. Los parámetros
        # requeridos para este tipo de consultas son `table`, `columns`, `values` y opcionalmente `conditions`.
        # Un ejemplo de consulta válida es el siguiente:
        # {
        #     "table": "usuarios",
        #     "columns": ["passwd"],
        #     "values": ["newPassword"]
        #     "conditions": [
        #         {
        #             "prefix": "WHERE",
        #             "operator": "=",
        #             "column": "email",
        #             "value": "ejemplo@correo.com"
        #         }
        #     ]
        # }
        # Lo cual produciría exactamente la siguiente consulta en sintaxis SQL:
        # UPDATE usuarios SET passwd = newPassword WHERE email = ejemplo@correo.com;
        # `statement` representa las variables que se van a procesar en la consulta.
        if len(parameters["columns"]) != len(parameters["values"]):
            # Si el número de columnas y de valores no coincide, lanza una excepción
            raise Exception("Number of columns and values doesn't coincide")
        
        table = parameters["table"]
        columns = parameters["columns"]
        values = parameters["values"]

        statement = []
        query: str = f"UPDATE {table} SET "

        for i in range(len(columns)):
            query += f"{columns[i]} = %s, "
            statement.append(values[i])
        
        # Elimina el `, ` del final.
        query = query[:-2]

        if not "conditions" in parameters:
            return query, statement

        conditions, condStmt = self.parseParameters(parameters["conditions"])

        query += conditions

        statement.extend(condStmt)
        
        return query, statement

    def prepareStatementDelete(self, parameters: dict) -> (str, list):
        # Genera la sintaxis SQL adecuada para una consulta de tipo DELETE. Los parámetros
        # requeridos para este tipo de consultas son `table` y opcionalmente `conditions`.
        # Un ejemplo de consulta válida es el siguiente:
        # {
        #     "table": "usuarios",
        #     "conditions": [
        #         {
        #             "prefix": "WHERE",
        #             "operator": "=",
        #             "column": "email",
        #             "value": "ejemplo@correo.com"
        #         }
        #     ]
        # }
        # Lo cual produciría exactamente la siguiente consulta en sintaxis SQL:
        # DELETE FROM usuarios WHERE email = ejemplo@correo.com;
        # `statement` representa las variables que se van a procesar en la consulta.
        table = parameters["table"]

        statement = []
        query: str = f"DELETE FROM {table}"

        if not "conditions" in parameters:
            return query, statement

        conditions, statement = self.parseParameters(parameters["conditions"])

        query += conditions
        
        return query, statement
        

    def selectAll(self, parameters: dict) -> tuple | None:
        query, statement = self.prepareStatementSelect(parameters)
        print(self.debug_query(query, statement))
        self.cursor.execute(query, statement)
        rows = self.cursor.fetchall()

        if not rows or len(rows) < 1: return None
        return tuple(rows)
    
    def selectOne(self, parameters: dict) -> dict | None:
        query, statement = self.prepareStatementSelect(parameters)
        self.cursor.execute(query, statement)
        row = self.cursor.fetchone()

        return row

    def insertOne(self, parameters: list) -> int:
        query, statement = self.prepareStatementInsert(parameters)
        self.cursor.execute(query, statement)
        self.db.commit()
        row = self.cursor.lastrowid

        return row

    def updateRows(self, parameters: list) -> int:
        query, statement = self.prepareStatementUpdate(parameters)
        self.cursor.execute(query, statement)
        self.db.commit()
        rows = self.cursor.rowcount

        return rows

    def deleteRows(self, parameters: int) -> int:
        query, statement = self.prepareStatementDelete(parameters)
        self.cursor.execute(query, statement)
        self.db.commit()
        rows = self.cursor.rowcount

        return rows
    
    def debug_query(self, query: str, params: list) -> str:
        q = query
        for p in params:
            q = q.replace("%s", repr(p), 1)
        return q