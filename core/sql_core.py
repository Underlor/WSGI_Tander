import sqlite3

from project_core import settings


def dict_fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SQLCore:
    def __init__(self, base_name='db'):
        self.connect = sqlite3.connect(settings.ROOT_DIR + '\\%s.sqlite' % (base_name,))
        self.init_base()

    def set_data_by_sql(self, sql, array=None):
        cursor = self.connect.cursor()

        if array:
            cursor.execute(sql % array)
        else:
            cursor.execute(sql)

        self.connect.commit()
        cursor.close()
        return True

    def get_data_by_sql(self, sql, array=None):
        cursor = self.connect.cursor()
        if array:
            cursor.execute(sql % array)
        else:
            cursor.execute(sql)

        result = dict_fetch(cursor)
        cursor.close()
        if len(result) != 0:
            return result

    def init_base(self):
        self.set_data_by_sql("""CREATE TABLE IF NOT EXISTS comments (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `last_name` VARCHAR(100) NOT NULL,
                          `first_name` VARCHAR(100) NOT NULL,
                          `middle_name` VARCHAR(100) NOT NULL,
                          `region` INTEGER NOT NULL,
                          `city` INTEGER NOT NULL,
                          `phone` VARCHAR(100) NOT NULL,
                          `email` VARCHAR(100) NOT NULL,
                          `text_comment` TEXT NOT NULL)""")

        self.set_data_by_sql("""CREATE TABLE IF NOT EXISTS regions (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `name` VARCHAR(100) NOT NULL)""")

        self.set_data_by_sql("""CREATE TABLE IF NOT EXISTS cites (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `region` INTEGER NOT NULL,
                          `name` VARCHAR(100) NOT NULL)""")

        if not self.get_data_by_sql("SELECT `id` FROM `regions`"):
            self.set_data_by_sql("""INSERT INTO regions(`name`) VALUES ('Краснодарский край'),
                                                                    ('Ростовская Область'),
                                                                    ('Ставропольский Край');""")

            self.set_data_by_sql("""INSERT INTO cites(`name`, `region`) VALUES('Краснодар', 1),
                                                                           ('Кропоткин', 1),
                                                                           ('Славянск', 1),
                                                                           ('Ростов', 2),
                                                                           ('Шахты', 2),
                                                                           ('Батайск', 2),
                                                                           ('Ставрополь', 3),
                                                                           ('Пятигорск', 3),
                                                                           ('Кисловодск', 3);""")

    def __del__(self):
        self.connect.close()


db = SQLCore(settings.DB_FILENAME)
