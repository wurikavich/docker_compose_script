# Тестовое задание №2 на должность Python-разработчика.

## Задание:
Необходимо создать и развернуть 2 Docker контейнера: БД PostgreSQL, Python-скрипт для взаимодействия с БД.
Разворачивается с помощью Docker Compose.

Алгоритм взаимодействия и работы скрипта:
- Скрипт каждую минуту генерирует и отправляет данные в БД.
    - "id" - id записи (инкремент)
    - "data" - сгенерированная строка данных
    - "date" - текущая дата и время
- Скрипт логирует свои действия.
- При достижении в таблице БД 30 строк, таблица должна очищаться и новые данные должны быть записаны 1-ой строчкой.

## Настройка и запуск:
Для развертывания проекта необходимо установить и запустить [Docker](https://www.docker.com/products/docker-desktop/).

1. Склонировать проект, перейти в папку docker_compose_script, при первом запуске настроить .env файл:
   ```bash
    git clone git@github.com:wurikavich/docker_compose_script.git     # склонировали проект
    cd docker_compose_script                                          # переместились в директорию проекта
    copy .env.dist .env                                               # создали файл .env 
   ```

2. Запуск Docker контейнеров:
    - Из директории docker_compose_script необходимо выполнить команду:
       ```bash
        docker-compose up               # команда для Windows  
        sudo docker-compose up          # команды для Linux-систем
       ```
    - Ждем выполнение команды, при успешном выполнении, в терминале должны быть следующие строчки:
       ```bash
        docker_compose_script-python-1    | 2023-07-21 18:20:17,789, INFO, Скрипт запущен., main, 98
        docker_compose_script-python-1    | 2023-07-21 18:20:17,792, INFO, Выполнено подключение К БД., main, 102
       ```

3. Остановка работы программы:
   ```bash
    docker-compose down                 # команда для Windows  
    sudo docker-compose down            # команды для Linux-систем
   ```

## Взаимодействие с БД:
Для работы с БД необходимо войти внутрь Docker контейнера с БД, выполнив команду:
```bash
 docker exec -it docker_compose_script-database-1   psql -U postgres -d postgres                 # команда для Windows  
 sudo docker exec -it docker_compose_script-database-1   psql -U postgres -d postgres            # команды для Linux-систем
```

В появившемся терминале необходимо вводить SQL-запросы:
```yaml
postgres=# Здесь вводим запрос
```

### Создание таблицы:
Таблица создается автоматически с помощью python-скрипта.

### Добавление записей в таблицу:
Записи в таблицу записываются в автоматическом режиме по заданному расписанию.

### Формирование выборки:

```bash
SELECT * FROM my_table; 
```

```yaml
postgres=# SELECT * FROM my_table;
id |              data              |            date
----+--------------------------------+----------------------------
1 | ssssssssssssssssssssssssssssss | 2023-07-21 18:05:01.518455
2 | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA | 2023-07-21 18:06:02.524893
3 | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | 2023-07-21 18:07:07.535161
4 | LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL | 2023-07-21 18:08:17.544364
5 | OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO | 2023-07-21 18:08:18.553862
(5 rows)
```

## Стек технологий
- Python 3.10
- PostgreSQL 11
- Docker-compose

## Разработчики
- [Александр Гетманов](https://github.com/wurikavich) - Backend