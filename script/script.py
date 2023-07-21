import logging
import sys
import time
from random import choice
from string import ascii_letters

import psycopg2

import config

logger = logging.getLogger(__name__)


def connect_base():
    """
    Выполняет подключение к БД.

    Возвращает объект подключения.
    """
    connect = psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )
    return connect


def create_table(connect, cursor, size: int = 30) -> None:
    """
    Создаёт таблицу в БД.
    Параметры:
        connect, cursor - Обязательные, необходимо для работы с БД
        size - Необязательный, длина текстового поля, по умолчанию 30 символов.
    """
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS my_table ("
        f"id SMALLSERIAL PRIMARY KEY, "
        f"data VARCHAR({size}) NOT NULL, "
        f"date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    )
    connect.commit()


def generate_date(length: int) -> str:
    """
    Генерирует строку для записи в БД.
    Параметры:
        length - Обязательный, длина строки.
    Возвращает объект типа "str" заданной длины.
    """
    return "".join(choice(ascii_letters) * length)


def insert_data(connect, cursor, value: str) -> None:
    """
    Добавляет одну запись в БД.
    Параметры:
        connect, cursor - Обязательные, необходимо для работы с БД.
        value - Обязательные, значение атрибута "data" для текущей записи.
    """
    cursor.execute(f"INSERT INTO my_table (data) VALUES ('{value}');")
    connect.commit()


def clearing_table(connect, cursor) -> None:
    """
    Очищает таблицу и сбрасывает счетчик поля id в БД.
    Параметры:
        connect, cursor -  Обязательные, необходимо для работы с БД.
    """
    cursor.execute("TRUNCATE my_table;")
    cursor.execute("ALTER SEQUENCE my_table_id_seq RESTART WITH 1;")
    connect.commit()


def check_environment() -> bool:
    """Проверяет доступность переменных окружения."""
    return all(
        [
            config.POSTGRES_DB,
            config.POSTGRES_USER,
            config.POSTGRES_PASSWORD,
            config.POSTGRES_HOST,
            config.POSTGRES_PORT
        ]
    )


def main():
    """Основная логика работы скрипта."""
    if not check_environment():
        logger.critical('Отсутствуют одна или несколько переменных окружения!')
        sys.exit('Отсутствуют одна или несколько переменных окружения!')

    logger.info('Скрипт запущен.')

    try:
        connect = connect_base()
        logger.info('Выполнено подключение К БД.')
        cursor = connect.cursor()
        create_table(connect, cursor, config.LENGTH_STRING)
        logger.info('Создана таблица.')
        count_record: int = 0
        while True:
            insert_data(connect, cursor, generate_date(config.LENGTH_STRING))
            count_record += 1
            logger.info(f'Добавлена запись в таблицу.')
            if count_record >= config.MAX_RECORDS:
                cursor.execute("SELECT COUNT(*) FROM my_table;")
                if cursor.fetchone()[0] >= config.MAX_RECORDS:
                    clearing_table(connect, cursor)
                    logger.info(f'Достигнуто максимальное количество записей - {count_record}.Таблица очищена.')
                    count_record: int = 0
            time.sleep(config.QUERY_RETRY_TIME)
    except Exception as error:
        logger.error(error, exc_info=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s,'
            ' %(levelname)s,'
            ' %(message)s,'
            ' %(funcName)s,'
            ' %(lineno)d'
        ),
        encoding='UTF-8',
        handlers=[
            logging.FileHandler('logs/main.log', mode='w', encoding='UTF-8'),
            logging.StreamHandler(sys.stdout),
        ],
    )

    time.sleep(config.STARTING_DATABASE)
    main()
