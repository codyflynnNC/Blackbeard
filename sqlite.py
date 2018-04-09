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
                       name text unique,
                       starting_season integer,
                       starting_episode integer,
                       active boolean default 1,
                       date_added timestamp default CURRENT_TIMESTAMP
               );"""

        create_episodes_table_sql = """
                   CREATE TABLE IF NOT EXISTS episodes (
                       episode_id integer PRIMARY KEY,
                       name text,
                       season integer,
                       number integer,
                       air_date datetime,
                       runtime decimal,
                       downloaded boolean default 0,
                       available boolean,
                       e_uid text unique,
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

    def get_show_id(self, name):
        sql = '''SELECT `id` from `shows` where name=?'''
        data = (name,)
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql, data)
            res = c.fetchone()
            return res[0]

    def get_episodes_to_download(self):
        sql = '''SELECT e.name, e.season, e.number, e.e_uid, s.name from episodes AS e
                 INNER JOIN shows AS s ON e.show_id = s.id
                 WHERE (e.downloaded=0 AND e.available=1) AND s.active=1'''

        with self.conn:
            c = self.conn.cursor()
            c.execute(sql)
            res = c.fetchall()
            return res

    def get_episode_id(self, name):
        sql = '''SELECT e_uid FROM episodes WHERE name = ?'''
        data = (name,)
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql, data)
            res = c.fetchall()
            return res

    def update_episode(self, e_uid):
        sql = '''UPDATE episodes SET downloaded=1 WHERE e_uid = ?'''
        data = (e_uid,)
        try:
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql, data)
        except sqlite3.Error as e:
            raise e

    def redownload_episode(self, e_uid):
        sql = ''' UPDATE episodes SET downloaded=0 WHERE e_uid = ?'''
        data = (e_uid,)
        try:
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql, data)
        except sqlite3.Error as e:
            raise e

    def make_episode_available(self, e_uid):
        sql = '''UPDATE episodes SET available=1 WHERE e_uid = ?'''
        data = (e_uid,)
        try:
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql, data)
        except sqlite3.Error as e:
            raise e

    def insert_show(self, name, starting_season, starting_episode):

        sql = '''INSERT INTO shows(`name`, `starting_season`, `starting_episode`) VALUES (?, ?, ?)'''
        data = (name, starting_season, starting_episode,)
        try:
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql, data)
        except sqlite3.IntegrityError:
            print('show already exists: {}'.format(name))

    def insert_episode(self, name, season, number, air_date, runtime, downloaded, available, show_id):

        sql = '''INSERT INTO episodes(name, season, number, air_date, runtime, downloaded, available, e_uid, show_id)
                 VALUES(?,?,?,?,?,?,?,?,?)'''

        e_uid = '{}_{}_S{}E{}'.format(show_id, name, season, number)
        data = (name, season, number, air_date, runtime, downloaded, available, e_uid, show_id,)
        try:
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql, data)
        except sqlite3.IntegrityError:
            print('episode already exists: {}'.format(name))

    def get_shows(self):
        sql = '''SELECT * from shows'''
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql)
            res = c.fetchall()
            return res

    def get_episodes_for_show(self, show_id):
        sql = '''SELECT * from episodes WHERE show_id=?'''
        data = (show_id,)
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql, data)
            res = c.fetchall()
            return res

    def get_all_episodes(self):
        sql = '''SELECT * from episodes'''
        with self.conn:
            c = self.conn.cursor()
            c.execute(sql)
            res = c.fetchall()
            return res


if __name__ == '__main__':
    sqlite = SQLiteDB()
    print(sqlite.get_episodes_for_show(sqlite.get_show_id('Silicon Valley')))
    pass
