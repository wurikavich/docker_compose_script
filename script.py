import os
import time

import psycopg2


def connect_base():
    connect = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return connect


def create_table(connect, cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            data VARCHAR(30),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    connect.commit()


def insert_table(connect, cursor):
    cursor.execute("insert into test_table (data) VALUES ('1'),('2'),('3'),('4'),('5'),('6'),('7'),('8')")
    connect.commit()


def truncate_table(connect, cursor):
    cursor.execute("TRUNCATE test_table")
    connect.commit()


def main():
    connect = connect_base()
    cursor = connect.cursor()
    create_table(connect, cursor)
    insert_table(connect, cursor)
    cursor.close()
    connect.close()


if __name__ == '__main__':
    time.sleep(20)
    main()
