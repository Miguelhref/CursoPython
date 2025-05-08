import os
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

from psycopg2.errors import UndefinedTable
# Cargamos las variables de entorno
load_dotenv()
conn = psycopg2.connect(
                        database=os.getenv('DATABASE_POSTGRES'),
                        host="",
                        user=os.getenv('USER_POSTGRES'),
                        password=os.getenv('PASSWORD_POSTGRES'),
                        port="5432"
                        )

conn.set_client_encoding('UTF8')

def table_exists(table_name):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute('SELECT EXISTS (SELECT table_name FROM information_schema.tables WHERE table_name = %s)', [table_name])

    table = cursor.fetchone()

    return table['exists']

def fetchone(sql, values = []):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(sql.strip(), values)

        return cursor.fetchone()
    except UndefinedTable as e:
        conn.rollback()

        raise e
    except Exception as e:
        conn.rollback()

        return None

def fetchall(sql, values = []):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(sql, values)

        return cursor.fetchall()
    except Exception as e:
        conn.rollback()

        raise e

def execute(sql, values = []):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(sql, values)

        conn.commit()

        if (sql.find("RETURNING") != -1):
            return cursor.fetchone()
        else:
            return True
    except Exception as e:
        conn.rollback()

        raise e