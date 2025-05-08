from src.database.postgres import table_exists, execute, fetchone, fetchall

class TokenRepo:
    def initialize():
        table = table_exists("tokens")

        print("Table tokens exists: ", table)

        if (not table):
            print("Creating table tokens")

            execute("""
                CREATE TABLE
                    tokens (
                        id serial PRIMARY KEY,
                        active BOOLEAN,
                        token TEXT NOT NULL,
                        name TEXT NOT NULL,
                        last_seen BIGINT
                    )
            """)

    def add(token, returning = '*'):
        sql = """
            INSERT INTO
                tokens (
                    active,
                    token,
                    name
                ) VALUES (%s, %s, %s) RETURNING {}""".format(returning)

        return execute(sql, [token['active'], token['token'], token['name']])

    def update(token_id, token, returning = '*'):
        sql = 'UPDATE tokens SET'
        values = []

        if token['name'] != None:
            sql += " name = '{}',"
            values.append(token['name'])

        if token['active'] != None:
            sql += " active = {},"
            values.append(token['active'])

        sql = sql[:-1] + " WHERE id = %s RETURNING {}".format(returning)
        values.append(token_id)

        return execute(sql, values)

    def delete(token_id):
        return execute("""
            DELETE FROM tokens WHERE id = %s RETURNING id
        """, [token_id])

    def list():
        return fetchall("""
            SELECT * FROM tokens ORDER BY id ASC
        """)

    def get_by_id(id):
        return fetchone("""
            SELECT * FROM tokens WHERE id = %s
        """, [id])

    def get_by_name(name):
        return fetchone("""
            SELECT * FROM tokens WHERE name = %s
        """, [name])

    def update_last_seen(token, last_seen):
        return execute("""
        UPDATE tokens SET last_seen = %s WHERE token = %s
        """, [last_seen, token])
