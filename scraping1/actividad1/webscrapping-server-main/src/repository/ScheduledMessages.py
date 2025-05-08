from src.database.postgres import table_exists, execute, fetchone, fetchall

class ScheduledMessagesRepo:
    def initialize():
        table = table_exists("scheduled_messages")

        print("Table scheduled_messages exists: ", table)

        if (not table):
            print("Creating table scheduled_messages")

            execute("""
                CREATE TABLE
                    scheduled_messages (
                        id serial PRIMARY KEY,
                        message TEXT NOT NULL,
                        tg_chatid BIGINT NOT NULL,
                        product_id INT NOT NULL,
                        store_id INT NOT NULL,
                        keyword_id INT references keywords(id)
                    )
            """)

    def add(scheduled_message):
        sql = """
            INSERT INTO
                scheduled_messages (
                    message,
                    tg_chatid,
                    product_id,
                    store_id,
                    keyword_id
                ) VALUES (%s, %s, %s, %s, %s) RETURNING id"""

        return execute(sql, [
            scheduled_message['message'],
            scheduled_message['tg_chatid'],
            scheduled_message['product_id'],
            scheduled_message['store_id'],
            scheduled_message['keyword_id']
        ])

    def delete(id):
        sql = """
            DELETE FROM
                scheduled_messages
            WHERE
                id = %s
        """

        return execute(sql, [id])

    def get_first(tg_chatid, select = "*"):
        sql = """
            SELECT
                {}
            FROM
                scheduled_messages
            WHERE
                tg_chatid = %s
            ORDER BY
                id ASC
            LIMIT 1
        """.format(select)

        return fetchone(sql, [tg_chatid])