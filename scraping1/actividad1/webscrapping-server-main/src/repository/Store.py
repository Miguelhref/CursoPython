from src.database.postgres import table_exists, execute, fetchone, fetchall

class StoreRepo:
    def initialize():
        table = table_exists("tiendas")

        print("Table tiendas exists: ", table)

        if (not table):
            print("Creating table tiendas")

            execute("""
                CREATE TABLE
                    tiendas (
                        id serial PRIMARY KEY,
                        name VARCHAR(250) unique not null,
                        active BOOLEAN NOT NULL,
                        tg_chatid BIGINT NOT NULL,
                        tg_chatid_bigdrop BIGINT,
                        percentage_bigdrop BIGINT
                    )
            """)

    def add(store):
        sql = """
            INSERT INTO
                tiendas (
                    name,
                    active,
                    tg_chatid,
                    tg_chatid_bigdrop,
                    percentage_bigdrop
                ) VALUES (%s, %s, %s, %s, %s) RETURNING id"""

        return execute(sql, [
            store['name'],
            store['active'],
            store['tg_chatid'],
            store['tg_chatid_bigdrop'],
            store['percentage_bigdrop']
        ])

    def update(id, store, returning = '*'):
        sql = 'UPDATE tiendas SET'
        values = []

        if store['name'] != None:
            sql += " name = %s,"
            values.append(store['name'])

        if store['active'] != None:
            sql += " active = %s,"
            values.append(store['active'])

        if store['tg_chatid'] != None:
            sql += " tg_chatid = %s,"
            values.append(store['tg_chatid'])

        if store['tg_chatid_bigdrop'] != None:
            sql += " tg_chatid_bigdrop = %s,"
            values.append(store['tg_chatid_bigdrop'])

        if store['percentage_bigdrop'] != None:
            sql += " percentage_bigdrop = %s,"
            values.append(store['percentage_bigdrop'])

        sql = sql[:-1]

        sql += ' WHERE id = %s RETURNING {}'.format(returning)
        values.append(id)

        return execute(sql, values)

    def delete(token_id, returning = "id"):
        return execute("""
            DELETE FROM tiendas WHERE id = %s RETURNING {}
        """.format(returning), [token_id])

    def list(select = '*'):
        return fetchall("""
            SELECT {} FROM tiendas ORDER BY id ASC
        """.format(select))

    def get_by_id(id, select = '*'):
        return fetchone("""
            SELECT {} FROM tiendas WHERE id = %s
        """.format(select), [id])

    def get_by_name(name, select = '*'):
        return fetchone("""
            SELECT {} FROM tiendas WHERE name = %s
        """.format(select), [name])

    def get_by_tg_chatid_or_tg_chatid_bigdrop(tg_chatid, select = "*"):
                return fetchall("""
            SELECT {} FROM tiendas WHERE tg_chatid = %s OR tg_chatid_bigdrop = %s
        """.format(select), [tg_chatid, tg_chatid])

