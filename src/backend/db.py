import os, mysql.connector

class Database():
    def __init__(self):
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

    def prepareStatementSelect(self, parameters: dict) -> (str, list):
        columns = ", ".join(parameters["columns"])
        table = parameters["table"]
        condition = parameters["condition"]["operator"]
        condColumn = parameters["condition"]["column"]
        condValue = parameters["condition"]["value"]

        query: str = f"SELECT {columns} FROM {table}"
        statement = []

        if "condition" in parameters:
            query += f" WHERE {condColumn} {condition} %s"
            statement.append(condValue)
        
        return query, statement

    def prepareStatementInsert(self, parameters: dict) -> (str, list):
        if len(parameters["columns"]) != len(parameters["values"]):
            raise Exception("Number of columns and values doesn't coincide")

        columns = "(" + ", ".join(parameters["columns"]) + ")"
        table = parameters["table"]
        values = parameters["values"]

        query: str = f"INSERT INTO {table} {columns} VALUES ("

        for _ in values:
            query +="%s, "
        
        query = query[:-2] + ")"

        print(query, " : ", values)

        return query, values

    def selectAll(self, parameters: dict) -> tuple | None:
        query, statement = self.prepareStatementSelect(parameters)
        self.cursor.execute(query, statement)
        rows = self.cursor.fetchall()

        if not rows or len(rows) < 1: return None
        return tuple(rows)
    
    def selectOne(self, parameters: dict) -> dict | None:
        query, statement = self.prepareStatementSelect(parameters)
        self.cursor.execute(query, statement)
        row = self.cursor.fetchone()

        return row

    def insertData(self, parameters: list) -> int:
        query, statement = self.prepareStatementInsert(parameters)
        self.cursor.execute(query, statement)
        self.db.commit()
        row = self.cursor.lastrowid

        return row
    
    def debug_query(self, query, params):
        q = query
        for p in params:
            q = q.replace("%s", repr(p), 1)
        return q