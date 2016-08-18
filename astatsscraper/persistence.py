from __future__ import division
import sqlite3
import datetime


class Persistor:
    def __init__(self, db_name='astatsscraper.db'):
        self.db_name = db_name

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.ensure_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def ensure_tables(self):
        # Make sure tables are present
        self.cursor.execute('''SELECT name FROM sqlite_master WHERE type = "table";''')
        tables = [table for (table,) in self.cursor.fetchall()]
        if 'users' in tables and 'owned_apps' in tables and 'steam_apps' in tables:
            return

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS steam_apps(
                                 app_id INTEGER,
                                 title VARCHAR(255),
                                 time_to_100 FLOAT,
                                 total_points FLOAT,
                                 points_per_time FLOAT,
                                 num_players INTEGER,
                                 num_players_to_100 INTEGER,
                                 percentage_of_players_to_100 FLOAT,
                                 astats_last_updated DATE,
                                 recent_steam_rating INTEGER,
                                 general_steam_rating INTEGER,
                                 steampowered_last_updated DATE,
                                 PRIMARY KEY (app_id)
                               );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                                 steam_id INTEGER,
                                 last_updated DATE,
                                 PRIMARY KEY (steam_id)
                               );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS owned_apps(
                                 steam_id INTEGER,
                                 app_id INTEGER,
                                 number_achieved INTEGER,
                                 percentage_achieved INTEGER,
                                 last_updated DATE,
                                 PRIMARY KEY (steam_id, app_id),
                                 FOREIGN KEY (steam_id) REFERENCES users(steam_id),
                                 FOREIGN KEY (app_id) REFERENCES steam_apps(app_id)
                               );''')

    def store_astats_app(self, atats_app_item):
        if atats_app_item.get('total_points') == 0:
            points_per_time = 0
        elif atats_app_item.get('time_to_100') == 0:
            points_per_time = None
        else:
            points_per_time = atats_app_item.get('total_points') / atats_app_item.get('time_to_100')
        if atats_app_item.get('num_players') == 0:
            percentage_to_hundo = 0
        else:
            percentage_to_hundo = atats_app_item.get('num_players_to_100') / atats_app_item.get('num_players')
        self.cursor.execute('''INSERT OR REPLACE INTO steam_apps (app_id, title, time_to_100, total_points,
                               points_per_time, num_players, num_players_to_100, percentage_of_players_to_100,
                               astats_last_updated, recent_steam_rating, general_steam_rating,
                               steampowered_last_updated)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                            (
                                atats_app_item.get('id'),
                                atats_app_item.get('title'),
                                atats_app_item.get('time_to_100'),
                                atats_app_item.get('total_points'),
                                points_per_time,
                                atats_app_item.get('num_players'),
                                atats_app_item.get('num_players_to_100'),
                                percentage_to_hundo,
                                datetime.datetime.now(),
                                None,
                                None,
                                None
                            ))
        self.connection.commit()

    def store_ownership(self, owned_app_item):
        self.cursor.execute('''INSERT OR IGNORE INTO steam_apps (app_id, title, time_to_100, total_points,
                               points_per_time, num_players, num_players_to_100, astats_last_updated,
                               recent_steam_rating, general_steam_rating, steampowered_last_updated)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                            (
                                owned_app_item.get('app_id'),
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                datetime.datetime.now(),
                                None,
                                None,
                                None,
                            ))
        self.cursor.execute('''INSERT OR REPLACE INTO users (steam_id, last_updated)
                               VALUES (?, ?);''',
                            (
                                owned_app_item.get('owner_id'),
                                datetime.datetime.now()
                            ))
        self.cursor.execute('''INSERT OR REPLACE INTO owned_apps (steam_id, app_id, number_achieved,
                               percentage_achieved, last_updated)
                               VALUES (?, ?, ?, ?, ?);''',
                            (
                                owned_app_item.get('owner_id'),
                                owned_app_item.get('app_id'),
                                owned_app_item.get('number_achieved'),
                                owned_app_item.get('percentage_achieved'),
                                datetime.datetime.now(),
                            ))
        self.connection.commit()

    def store_app_id(self, app_item):
        self.cursor.execute('''INSERT OR REPLACE INTO steam_apps (app_id, title, time_to_100, total_points,
                               points_per_time, num_players, num_players_to_100, percentage_of_players_to_100,
                               astats_last_updated, recent_steam_rating, general_steam_rating,
                               steampowered_last_updated)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                            (
                                app_item.get('id'),
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                            ))
        self.connection.commit()

    def get_all_app_ids(self):
        self.cursor.execute('SELECT app_id FROM steam_apps;')
        values = self.cursor.fetchall()
        ids = [id for (id,) in values]
        return ids

    def get_app_ids_for_unknown_points(self):
        self.cursor.execute('SELECT app_id FROM steam_apps where total_points IS NULL;')
        values = self.cursor.fetchall()
        ids = [id for (id,) in values]
        return ids

    def get_app_ids_for_apps_with_points(self):
        self.cursor.execute('SELECT app_id FROM steam_apps where total_points > 0;')
        values = self.cursor.fetchall()
        ids = [id for (id,) in values]
        return ids

    def get_app_ids_sorted_by_points_per_time(self):
        self.cursor.execute('SELECT app_id FROM steam_apps ORDER BY points_per_time DESC;')
        values = self.cursor.fetchall()
        ids = [id for (id,) in values]
        return ids

    def get_owned_app_ids(self, owner_id):
        self.cursor.execute('SELECT app_id FROM owned_apps WHERE steam_id=?;', (owner_id,))
        values = self.cursor.fetchall()
        ids = [id for (id,) in values]
        return ids

    def get_owned_app_info(self, owner_id, order_by=None, asc_desc=None):
        query_string = 'SELECT steam_apps.app_id, title, time_to_100, total_points, points_per_time, num_players, ' \
                       'num_players_to_100, percentage_of_players_to_100, steam_apps.astats_last_updated,' \
                       'recent_steam_rating, general_steam_rating, steampowered_last_updated' \
                       'FROM steam_apps INNER JOIN owned_apps ON steam_apps.app_id = owned_apps.app_id WHERE ' \
                       'owned_apps.steam_id = ?'
        query_params = (owner_id,)
        if order_by:
            query_string += ' ORDER BY ?'
            if asc_desc:
                query_params = (order_by + ' ' + asc_desc,)
            else:
                query_params = (order_by,)
        query_string += ';'

        self.cursor.execute(query_string, query_params)
        values = self.cursor.fetchall()
        return values

    def get_all_apps_info(self, order_by=None, asc_desc=None):
        query_string = 'SELECT app_id, title, time_to_100, total_points, points_per_time, num_players, ' \
                       'num_players_to_100, percentage_of_players_to_100, astats_last_updated, recent_steam_rating,' \
                       'general_steam_rating, steampowered_last_updated FROM steam_apps'
        query_params = ()
        if order_by:
            query_string += ' ORDER BY ?'
            if asc_desc:
                query_params = (order_by + ' ' + asc_desc,)
            else:
                query_params = (order_by,)
        query_string += ';'
        self.cursor.execute(query_string, query_params)
        values = self.cursor.fetchall()
        return values
