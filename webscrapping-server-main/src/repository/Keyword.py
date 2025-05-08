from src.database.postgres import table_exists, execute, fetchone, fetchall

class KeywordRepo:
    def initialize():
        table = table_exists("keywords")

        print("Table keywords exists: ", table)

        if (not table):
            print("Creating table keywords")

            execute("""
                CREATE TABLE
                    keywords (
                        id serial PRIMARY KEY,
                        porcentage INT not null,
                        keyword TEXT NOT NULL,
                        max_page INT not null,
                        last_checked BIGINT,
                        store_id INT references tiendas(id),
                        active boolean not null,
                        alert_new BOOLEAN,
                        category TEXT,
                        blacklist TEXT,
                        sort TEXT,
                        landing_url TEXT
                    )
            """)

    def add(keyword):
        sql = """
            INSERT INTO
                keywords (
                    porcentage,
                    keyword,
                    max_page,
                    store_id,
                    active,
                    alert_new,
                    category,
                    blacklist,
                    sort,
                    landing_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""

        return execute(sql, [
            keyword['porcentage'],
            keyword['keyword'],
            keyword['max_page'],
            keyword['store_id'],
            keyword['active'],
            keyword['alert_new'],
            keyword['category'],
            keyword['blacklist'],
            keyword['sort'],
            keyword['landing_url']
        ])

    def update(id, update, returning = '*'):
        sql = 'UPDATE keywords SET'
        values = []

        if update['porcentage'] != None:
            sql += " porcentage = %s,"
            values.append(update['porcentage'])
        
        if update['keyword'] != None:
            sql += " keyword = %s,"
            values.append(update['keyword'])
        
        if update['max_page'] != None:
            sql += " max_page = %s,"
            values.append(update['max_page'])

        if update['store_id'] != None:
            sql += " store_id = %s,"
            values.append(update['store_id'])

        if update['active'] != None:
            sql += " active = %s,"
            values.append(update['active'])

        if update['alert_new'] != None:
            sql += " alert_new = %s,"
            values.append(update['alert_new'])

        if update['category'] != None:
            sql += " category = %s,"
            values.append(update['category'])

        if update['blacklist'] != None:
            sql += " blacklist = %s,"
            values.append(update['blacklist'])

        if update['sort'] != None:
            sql += " sort = %s,"
            values.append(update['sort'])

        if update['landing_url'] != None:
            sql += " landing_url = %s,"
            values.append(update['landing_url'])

        sql = sql[:-1]

        sql += ' WHERE id = %s RETURNING {}'.format(returning)
        values.append(id)

        return execute(sql, values)

    def delete(token_id):
        return execute("""
            DELETE FROM keywords WHERE id = %s RETURNING id
        """, [token_id])

    def list():
        return fetchall("""
            SELECT * FROM keywords ORDER BY id ASC
        """)

    def get_by_id(id, select = '*'):
        return fetchone("""
            SELECT {} FROM keywords WHERE id = %s
        """.format(select), [id])

    def keyword_exists_for_store(keyword, store_id, exclude_id = None):
        slq = """
            SELECT EXISTS (SELECT 1 FROM keywords WHERE keyword = %s AND store_id = %s
        """
        values = [keyword, store_id]

        if (exclude_id != None):
            slq += " AND id != %s"
            values.append(exclude_id)

        slq += ");"

        return fetchone(slq, values)['exists']

    def get_by_store_id_first_last_checked(store_id):
        return fetchone("""
            SELECT * from keywords WHERE store_id = %s AND active = true ORDER BY last_checked NULLS FIRST
        """, [store_id])

    def update_last_checked(id, last_checked):
        return execute("""
            UPDATE keywords SET last_checked = %s WHERE id = %s RETURNING *
        """, [last_checked, id])

    def get_keyword_join_store(keyword_id):
        return fetchone("""
            SELECT
                k.id as keyword_id,
                k.active as keyword_active,
                k.alert_new as keyword_alert_new,
                k.blacklist as keyword_blacklist,
                k.porcentage as keyword_porcentage,
                k.keyword,
                t.id as store_id,
                t.active as store_active,
                t.tg_chatid,
                t.tg_chatid_bigdrop,
                t.percentage_bigdrop
            FROM
                keywords k
            INNER JOIN
                tiendas t
            ON
                 k.store_id = t.id
            WHERE
                k.id = %s
        """, [keyword_id])
    def get_by_store_id(store_id, select='*'):
        return fetchall("""
            SELECT {} FROM keywords WHERE store_id = %s
        """.format(select), [store_id])
