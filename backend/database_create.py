import psycopg2
import random

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='wlAc2vR1ms5fBaPtvIM0',
    host='localhost',
    port='5434'
)

cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            breed VARCHAR(100),
            age INTEGER,
            available BOOLEAN
        )
    """)
    conn.commit()

def main():
    create_table()

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()