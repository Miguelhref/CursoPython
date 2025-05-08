from src.database.postgres import table_exists, execute, fetchone, fetchall

class WesternDigitalRepo:
    def initialize():
        table = table_exists("western_digital")

        print("Table western_digital exists: ", table)

        if (not table):
            print("Creating table western_digital")

            execute("""
                CREATE TABLE
                    western_digital (
                        id serial PRIMARY KEY,
                        code TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        price NUMERIC(12, 2),
                        stock_level INT,
                        last_price_changed BIGINT
                    )
            """)

    def add(product, returning = '*'):
        sql = """
            INSERT INTO
                western_digital (
                    code,
                    name,
                    price,
                    stock_level
                ) VALUES (%s, %s, %s, %s) RETURNING {}""".format(returning)

        return execute(sql, [product['code'], product['name'], product['price'], product['stock_level']])

    def update(code, product, returning = '*'):
        sql = 'UPDATE western_digital SET'
        values = []

        if product['name'] != None:
            sql += " name = '{}',"
            values.append(product['name'])

        if product['price'] != None:
            sql += " price = {},"
            values.append(product['price'])

        if product['stock_level'] != None:
            sql += " stock_level = {},"
            values.append(product['stock_level'])

        if product['last_price_changed'] != None:
            sql += " last_price_changed = {},"
            values.append(product['last_price_changed'])

        sql = sql[:-1] + " WHERE code = %s"
        values.append(code)

        if returning != None:
            sql += " RETURNING {}".format(returning)

        return execute(sql, values)

    def get_by_code(code, select = "*"):
        return fetchone("""
            SELECT {} FROM western_digital WHERE code = %s
        """.format(select), [code])