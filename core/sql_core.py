import sqlite3

import os

from project_core import settings


def dict_fetch(cursor):
    """
    Собирает словарь путем слияния строк и имен колонок в словарь
    :param cursor: sql объект с данными
    :return: словарь с данными
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SQLCore:
    """
        Ядро обработчик SQL запросов
    """

    def __init__(self, base_name='db'):
        db_file = settings.ROOT_DIR + '\\%s.sqlite' % (base_name,)

        if not os.path.isfile(db_file):
            self.connect = sqlite3.connect(db_file)
            self.base_init()
        else:
            self.connect = sqlite3.connect(db_file)

    def set_data_by_sql(self, sql, array=None):
        """
            Обработка запроса на изменения таблицы
        :param sql: запрос
        :param array: опционально массив с передаваемыми данными в запрос
        :return: успешность выполнения
        """
        cursor = self.connect.cursor()
        if array:
            cursor.execute(sql % array)
        else:
            cursor.execute(sql)

        self.connect.commit()
        cursor.close()
        return True

    def get_data_by_sql(self, sql, array=None):
        """
            Обработка запроса на получение данных из таблици
        :param sql: запрос
        :param array: опционально массив с передаваемыми данными в запрос
        :return:
        """
        cursor = self.connect.cursor()
        if array:
            cursor.execute(sql % array)
        else:
            cursor.execute(sql)

        result = dict_fetch(cursor)
        cursor.close()

        if len(result) != 0:
            return result

    def base_init(self):
        """
            Инициализация базы, если ее нет.
        """
        self.set_data_by_sql("""CREATE TABLE comments (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `last_name` VARCHAR(100) NOT NULL,
                          `first_name` VARCHAR(100) NOT NULL,
                          `middle_name` VARCHAR(100) NOT NULL,
                          `region` INTEGER NOT NULL,
                          `city` INTEGER NOT NULL,
                          `phone` VARCHAR(100) NOT NULL,
                          `email` VARCHAR(100) NOT NULL,
                          `text_comment` TEXT NOT NULL)""")

        self.set_data_by_sql("""CREATE TABLE cities (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `region` INTEGER NOT NULL,
                          `name` VARCHAR(100) NOT NULL)""")

        self.set_data_by_sql("""CREATE TABLE regions (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `name` VARCHAR(100) NOT NULL)""")

        self.set_data_by_sql("""INSERT INTO regions(`name`) VALUES ('Челябинская Область'),
                                                                ('Свердловская область'),
                                                                ('Ростовская Область'),
                                                                ('Краснодарский край');""")

        self.set_data_by_sql("""INSERT INTO cities(`name`, `region`) VALUES('Снежинск', 1),
                                                                       ('Челябинск', 1),
                                                                       ('Кыштым', 1),
                                                                       ('Касли', 1),
                                                                       ('Копейск', 1),
                                                                       ('Екатеринбург', 2),
                                                                       ('Верхний тагил', 2),
                                                                       ('Заречный', 2),
                                                                       ('Ростов', 3),
                                                                       ('Шахты', 3),
                                                                       ('Батайск', 3),
                                                                       ('Краснодар', 4),
                                                                       ('Кропоткин', 4),
                                                                       ('Славянск', 4);""")

    def __del__(self):
        self.connect.close()


db = SQLCore(settings.DB_FILENAME)
