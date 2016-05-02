import sqlite3


class Persistor:
    def __init__(self):
        self.connection = sqlite3.connect('astatsscraper.db')
        self.cursor = self.connection.cursor()

    def init_database(self):
        self.cursor.execute('''CREATE TABLE steam_apps(
                                 app_id INTEGER,
                                 title VARCHAR(255),
                                 time_to_100 FLOAT,
                                 total_points FLOAT
                               )''')
