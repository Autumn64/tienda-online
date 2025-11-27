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

    def selectAll(self, query: str, parameters: list) -> tuple | None:
        self.cursor.execute(query, parameters)
        rows = self.cursor.fetchall()
        self.disconnect()

        if not rows or len(rows) < 1: return None
        return tuple(rows)
    
    def selectOne(self, query: str, parameters: list) -> dict | None:
        self.cursor.execute(query, parameters)
        row = self.cursor.fetchone()
        self.disconnect()

        return row
    
    