from __future__ import division
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import datetime

Base = sqlalchemy.ext.declarative.declarative_base()

class Steamapp(Base):
    __tablename__ = 'steam_apps'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    time_to_100 = sqlalchemy.Column(sqlalchemy.Float)
    total_points = sqlalchemy.Column(sqlalchemy.Float)
    points_per_time = sqlalchemy.Column(sqlalchemy.Float)
    num_players = sqlalchemy.Column(sqlalchemy.Integer)
    num_players_to_100 = sqlalchemy.Column(sqlalchemy.Integer)
    percentage_of_players_to_100 = sqlalchemy.Column(sqlalchemy.Float)
    astats_last_updated = sqlalchemy.Column(sqlalchemy.Date)
    recent_steam_rating = sqlalchemy.Column(sqlalchemy.Integer)
    overall_steam_rating = sqlalchemy.Column(sqlalchemy.Integer)
    steampowered_last_updated = sqlalchemy.Column(sqlalchemy.Date)


class User(Base):
    __tablename__ = 'users'

    steam_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    last_updated = sqlalchemy.Column(sqlalchemy.Date)


class OwnedApp(Base):
    __tablename__ = 'owned_apps'

    steam_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.steam_id', primary_key=True))
    app_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('steamapps.id'), primary_key=True)
    number_achieved = sqlalchemy.Column(sqlalchemy.Integer)
    percentage_achieved = sqlalchemy.Column(sqlalchemy.Integer)
    last_updated = sqlalchemy.Column(sqlalchemy.Date)


class Persistor:
    def __init__(self, db_name='astatsscraper.db'):
        self.db_name = db_name

    def __enter__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///{}'.format(self.db_name))
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.commit()
        self.session.close()

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
        app = Steamapp(id=atats_app_item.get('id'),
                       title=atats_app_item.get('title'),
                       time_to_100=atats_app_item.get('time_to_100'),
                       total_points=atats_app_item.get('total_points'),
                       points_per_time=points_per_time,
                       num_players=atats_app_item.get('num_players'),
                       num_players_to_100=atats_app_item.get('num_players_to_100'),
                       percentage_of_players_to_100=percentage_to_hundo,
                       astats_last_updated=datetime.datetime.now(),
                       )
        self.session.add(app)

    def store_ownership(self, owned_app_item):
        app = Steamapp(id=owned_app_item.get('app_id'))
        self.session.add(app)
        user = User(steam_id=owned_app_item.get('owner_id'), last_updated=datetime.datetime.now())
        self.session.add(user)
        owned_app = OwnedApp(steam_id=owned_app_item.get('owner_id'),
                             app_id=owned_app_item.get('app_id'),
                             number_achieved=owned_app_item.get('number_achieved'),
                             percentage_achieved=owned_app_item.get('percentage_achieved'),
                             last_updated=datetime.datetime.now()
                             )
        self.session.add(owned_app)


    def store_app_id(self, app_item):
        app = Steamapp(id=app_item.get('app_id'))
        self.session.add(app)

    def get_all_app_ids(self):
        ids = [id for id in self.session.query(Steamapp.id)]
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
