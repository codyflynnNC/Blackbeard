import sqlite3


class SQLiteDB:
    def __init__(self):
        self.db = 'sqlitedb'
        self.conn = self._connect()
        self._set_up_env()

    def _connect(self):
        try:
            conn = sqlite3.connect(self.db)
            return conn
        except sqlite3.Error as e:
            print(e)
        return None

    def _set_up_env(self):
        create_shows_table_sql = """
                   CREATE TABLE IF NOT EXISTS shows (
                       id integer PRIMARY KEY,
                       name text,
                       date_added timestamp default CURRENT_TIMESTAMP,
                       active boolean default 1
               );"""

        create_episodes_table_sql = """
                   CREATE TABLE IF NOT EXISTS episodes (
                       episode_id integer PRIMARY KEY,
                       name text,
                       season integer,
                       number integer,
                       air_date datetime,
                       runtime decimal,
                       downloaded boolean,
                       available boolean,
                       show_id integer,
                       FOREIGN KEY (show_id) REFERENCES shows (id)
               );"""
        with self.conn:
            try:
                c = self.conn.cursor()
                c.execute(create_shows_table_sql)
                c.execute(create_episodes_table_sql)
            except sqlite3.Error as e:
                print(e)

    def insert_show(self, show_name):
        sql = '''INSERT INTO shows(name) VALUES (?)'''
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql, show_name)

    def insert_episode(self, name, season, number, air_date, runtime, downloaded, available, show_id):
        sql = '''INSERT INTO episodes(name, season, number, air_date, runtime, downloaded, available, show_id)
                 VALUES(?,?,?,?,?,?,?,?)'''

        data = (name, season, number, air_date, runtime, downloaded, available, show_id)
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql)

    def get_shows(self):
        sql = '''SELECT * from shows'''
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql)
            res = c.fetchall()
            for row in res:
                print(row)

    def get_show_id(self, name):
        sql = "SELECT id from shows where name=?"
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql, name)
            res = c.fetchone()
            return res[0]


if __name__ == '__main__':
    sqlite = SQLiteDB()
    sqlite.insert_show(('test_show4',))
    sqlite.get_show_id(('test_show',))
    pass
