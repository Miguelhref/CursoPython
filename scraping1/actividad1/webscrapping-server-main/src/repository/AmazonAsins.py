from src.database.postgres import table_exists, execute, fetchone, fetchall

class AmazonAsinsRepo:
    def initialize():
        countries = ['es', 'it', 'de', 'fr', 'uk']

        for country in countries:
            table_name = 'amazon_asins_' + country
            table = table_exists(table_name)

            print(f"Table {table_name} exists: ", table)

            if (not table):
                print(f"Creating table {table_name}")

                execute(f"""
                    CREATE TABLE
                        {table_name} (
                            id serial PRIMARY KEY,
                            asin TEXT UNIQUE NOT NULL,
                            name TEXT NOT NULL,
                            price_new NUMERIC(12, 2),
                            price_reaco NUMERIC(12, 2),
                            pvp NUMERIC(12, 2),
                            price_new_alert NUMERIC(12, 2) NOT NULL,
                            price_reaco_alert NUMERIC(12, 2) NOT NULL,
                            last_price_changed BIGINT,
                            last_notified BIGINT,
                            active BOOLEAN,
                            last_checked BIGINT
                        )
                """)

    def add(amazon_asin, table):
        sql = f"""
            INSERT INTO
                {table} (
                    asin,
                    name,
                    price_new_alert,
                    price_reaco_alert,
                    active
                ) VALUES (%s, %s, %s, %s, %s) RETURNING id"""

        return execute(sql, [
            amazon_asin['asin'],
            amazon_asin['name'],
            amazon_asin['price_new_alert'],
            amazon_asin['price_reaco_alert'],
            amazon_asin['active']
        ])

    def update(id, table, amazon_asin, returning = '*'):
        sql = f'UPDATE {table} SET'
        values = []

        if ('asin' in amazon_asin and amazon_asin['asin'] != None):
            sql += " asin = %s,"
            values.append(amazon_asin['asin'])

        if ('name' in amazon_asin and amazon_asin['name'] != None):
            sql += " name = %s,"
            values.append(amazon_asin['name'])

        if ('price_new' in amazon_asin and amazon_asin['price_new'] != None):
            sql += " price_new = %s,"
            values.append(amazon_asin['price_new'])

        if ('price_reaco' in amazon_asin and amazon_asin['price_reaco'] != None):
            sql += " price_reaco = %s,"
            values.append(amazon_asin['price_reaco'])

        if ('pvp' in amazon_asin and amazon_asin['pvp'] != None):
            sql += " pvp = %s,"
            values.append(amazon_asin['pvp'])

        if ('price_new_alert' in amazon_asin and amazon_asin['price_new_alert'] != None):
            sql += " price_new_alert = %s,"
            values.append(amazon_asin['price_new_alert'])

        if ('price_reaco_alert' in amazon_asin and amazon_asin['price_reaco_alert'] != None):
            sql += " price_reaco_alert = %s,"
            values.append(amazon_asin['price_reaco_alert'])

        if ('last_price_changed' in amazon_asin and amazon_asin['last_price_changed'] != None):
            sql += " last_price_changed = %s,"
            values.append(amazon_asin['last_price_changed'])

        if ('last_notified' in amazon_asin and amazon_asin['last_notified'] != None):
            sql += " last_notified = %s,"
            values.append(amazon_asin['last_notified'])

        if ('active' in amazon_asin and amazon_asin['active'] != None):
            sql += " active = %s,"
            values.append(amazon_asin['active'])

        if ('last_checked' in amazon_asin and amazon_asin['last_checked'] != None):
            sql += " last_checked = %s,"
            values.append(amazon_asin['last_checked'])

        sql = sql[:-1]

        sql += " WHERE asin = %s"
        values.append(amazon_asin['asin'])

        if returning != None:
            sql += " RETURNING {}".format(returning)

        return execute(sql, values)

    def delete_by_asin(asin, table):
        sql = f"DELETE FROM {table} WHERE asin = %s RETURNING id"

        return execute(sql, [asin])

    def list(table):
        sql = f"SELECT * FROM {table}"

        return fetchall(sql)

    def get_by_asin(asin, table):
        sql = f"SELECT * FROM {table} WHERE asin = %s"

        return fetchone(sql, [asin])

    def get_all_active_by_last_checked(table):
        sql = f"SELECT * FROM {table} WHERE active = true ORDER BY last_checked NULLS FIRST"

        return fetchall(sql)

    def update_last_checked(asin, last_checked, table):
        sql = f"UPDATE {table} SET last_checked = %s WHERE asin = %s"

        return execute(sql, [last_checked, asin])

    def update_last_notified(id, last_notified, table):
        sql = f"UPDATE {table} SET last_notified = %s WHERE id = %s"

        return execute(sql, [last_notified, id])
    
