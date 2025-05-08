from src.database.postgres import table_exists, execute, fetchone, fetchall

class ProductRepo:
    def initialize():
        table = table_exists("productos")

        print("Table productos exists: ", table)

        if (not table):
            print("Creating table productos")

            execute("""
                CREATE TABLE
                    productos (
                        id serial PRIMARY KEY,
                        sku TEXT NOT NULL,
                        url_item TEXT NOT NULL,
                        url_img TEXT, 
                        name TEXT NOT NULL,
                        price NUMERIC(12, 2) NOT NULL,
                        pvp NUMERIC(12, 2),
                        last_price_changed BIGINT,
                        last_notified BIGINT,
                        store_id INT references tiendas(id) NOT NULL,
                        last_seen BIGINT
                    )
            """)

    def add(product):
        sql = """
            INSERT INTO
                productos (
                    sku,
                    url_item,
                    url_img,
                    name,
                    price,
                    pvp,
                    last_price_changed,
                    last_notified,
                    store_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""

        return execute(sql, [
            product['sku'],
            product['url_item'],
            product['url_img'],
            product['name'],
            product['price'],
            product['pvp'],
            product['last_price_changed'],
            product['last_notified'],
            product['store_id']
        ])

    def update(sku, store_id, product, returning = '*'):
        sql = 'UPDATE productos SET'
        values = []

        if product['url_item'] != None:
            sql += " url_item = %s,"
            values.append(product['url_item'])

        if product['url_img'] != None:
            sql += " url_img = %s,"
            values.append(product['url_img'])

        if product['name'] != None:
            sql += " name = %s,"
            values.append(product['name'])

        if product['price'] != None:
            sql += " price = %s,"
            values.append(product['price'])

        if product['pvp'] != None:
            sql += " pvp = %s,"
            values.append(product['pvp'])

        if product['last_price_changed'] != None:
            sql += " last_price_changed = %s,"
            values.append(product['last_price_changed'])

        if product['last_notified'] != None:
            sql += " last_notified = %s,"
            values.append(product['last_notified'])

        sql = sql[:-1]

        sql += " WHERE store_id = %s AND sku = %s"

        values.append(store_id)
        values.append(sku)


        if returning != None:
            sql += " RETURNING {}".format(returning)

        return execute(sql, values)

    def get_by_sku(sku, store_id, select = '*'):
        return fetchone("""
            SELECT {} FROM productos WHERE sku = %s AND store_id = %s
        """.format(select), [sku, store_id])

    def get_by_sku_and_store_id(sku, store_id):
        return fetchone("""
            SELECT * FROM productos WHERE sku = %s AND store_id = %s
        """, [sku, store_id])

    def update_last_notified(id, last_notified):
        sql = """
            UPDATE
                productos
            SET
                last_notified = %s
            WHERE
                id = %s
        """

        return execute(sql, [last_notified, id])

    def update_last_seen(id, last_seen):
        sql = """
            UPDATE
                productos
            SET
                last_seen = %s
            WHERE
                id = %s
        """

        return execute(sql, [last_seen, id])