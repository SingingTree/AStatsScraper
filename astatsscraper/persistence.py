import sqlite3


class Persistor:
    def __enter__(self):
        self.connection = sqlite3.connect('astatsscraper.db')
        self.cursor = self.connection.cursor()
        # Maybe find a better way than ensuring each time
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def ensure_tables(self):
        print("ENSURING TABLES")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS steam_apps(
                                 app_id INTEGER,
                                 title VARCHAR(255),
                                 time_to_100 FLOAT,
                                 total_points FLOAT,
                                 PRIMARY KEY (app_id)
                               );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                                 steam_id INTEGER,
                                 PRIMARY KEY (steam_id)
                               );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS owned_app(
                                 steam_id INTEGER,
                                 app_id INTEGER,
                                 PRIMARY KEY (steam_id, app_id),
                                 FOREIGN KEY (steam_id) REFERENCES users(steam_id)
                                 FOREIGN KEY (app_id) REFERENCES steam_apps(app_id)
                               );''')

    def store_app(self, app_item):
        self.cursor.execute('''INSERT OR REPLACE INTO steam_apps (app_id, title, time_to_100, total_points)
                                VALUES (?, ?, ?, ?);''',
                            (
                                app_item.get('id'),
                                app_item.get('title'),
                                app_item.get('time_to_100'),
                                app_item.get('total_points'),
                            ))
        self.connection.commit()

    def store_ownership(self, owned_app_item):
        self.cursor.execute('''INSERT OR IGNORE INTO steam_apps (app_id, title, time_to_100, total_points)
                                VALUES (?, ?, ?, ?);''',
                            (
                                owned_app_item.get('app_id'),
                                None,
                                None,
                                None
                            ))
        self.cursor.execute('''INSERT OR IGNORE INTO users (steam_id)
                               VALUES (?);''',
                            (
                                owned_app_item.get('owner_id'),
                            ))
        self.cursor.execute('''INSERT OR IGNORE INTO owned_app (steam_id, app_id)
                               VALUES (?, ?);''',
                            (
                                owned_app_item.get('owner_id'),
                                owned_app_item.get('app_id'),
                            ))
        self.connection.commit()

