import psycopg2


class DatabaseConnection:

    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="db",
            port="5432",
            database="postgres"
        )

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if query.split()[0].lower() == "select":
                return cursor.fetchall()
            self.connection.commit()

    def close(self):
        self.connection.close()
