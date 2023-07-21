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


def compare_count(connect, cursor, count_record: int) -> int:
    """
    Сравнивает количество созданных записей с фактическим количеством в таблице.
    Параметры:
        connect, cursor -  Обязательные, необходимо для работы с БД.
        count_record - Обязательные, количество созданных записей.
    Возвращает обнуленный счетчик, если количество созданных записей равно фактическим.
    В противном случае останавливает программу с сообщением об ошибке.
    """
    cursor.execute("SELECT COUNT(*) FROM my_table;")
    table_records = cursor.fetchone()[0]
    if table_records == config.MAX_RECORDS:
        clearing_table(connect, cursor)
        logger.info(
            f"Количество записей в таблице - {table_records}. "
            f"Максимально допустимое количество записей {config.MAX_RECORDS}. "
            f"Все записи были удалены. Счетчик id записи пошел с 1."
        )
        count_record: int = 0
        return count_record
    elif table_records != config.MAX_RECORDS:
        message = (
            f"Ошибка! Количество записей созданных программой ({count_record})"
            f" не соответствует количеству записей в таблице ({table_records})!"
        )
    else:
        message = (
            f"Ошибка при попытке сравнения количества записей!"
            f"Программа создала {count_record} записей в таблицу. "
            f"Фактических записей в таблице - {table_records})!"
        )
    logger.critical(message)
    sys.exit(message)


def main():
    """Основная логика работы скрипта."""
    if not check_environment():
        logger.critical("Отсутствуют одна или несколько переменных окружения!")
        sys.exit("Отсутствуют одна или несколько переменных окружения!")

    logger.info("Cкрипт запущен.")

    try:
        connect = connect_base()
        logger.info("Выполнено подключение К БД.")
        cursor = connect.cursor()
        create_table(connect, cursor, config.LENGTH_STRING)
        logger.info("Создана таблица.")
        count_record: int = 0
        while True:
            insert_data(connect, cursor, generate_date(config.LENGTH_STRING))
            count_record += 1
            logger.info(f"Добавлена запись в таблицу. Количество записей в таблице - {count_record}.")
            time.sleep(config.QUERY_RETRY_TIME)
            if count_record < config.MAX_RECORDS:
                continue
            count_record = compare_count(connect, cursor, count_record)
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
