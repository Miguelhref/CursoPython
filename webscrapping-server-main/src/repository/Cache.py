from src.database.postgres import table_exists, execute, fetchone, fetchall

class CacheRepo:
    def initialize():
        table = table_exists("cache")

        print("Table cache exists: ", table)

        if (not table):
            print("Creating table cache")

            execute("""
                CREATE TABLE
                    cache (
                        id serial PRIMARY KEY, 
                        sku TEXT NOT NULL,
                        price NUMERIC(12, 2) NOT NULL,
                        old_price NUMERIC(12, 2),
                        store_id INT references tiendas(id) NOT NULL,
                        timestamp BIGINT
                    )
            """)

    def add(cache):
        sql = """
            INSERT INTO
                cache (
                    sku,
                    price,
                    old_price,
                    store_id
                ) VALUES (%s, %s, %s, %s) RETURNING *"""

        return execute(sql, [cache['sku'], cache['price'], cache['old_price'], cache['store_id']])

    def get_by_sku_and_price(sku, price, store_id, select = '*'):
        return fetchone("""
            SELECT {} FROM cache WHERE sku = %s AND price = %s AND store_id = %s
        """.format(select), [sku, price, store_id])

    def update_old_price(id, old_price):
        return execute("""
            UPDATE cache SET old_price = %s WHERE id = %s
        """, [old_price, id])
    
    def update_timestamp(id, timestamp):
        return execute("""
            UPDATE cache SET timestamp = %s WHERE id = %s
        """, [timestamp, id])