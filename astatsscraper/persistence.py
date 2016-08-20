from __future__ import division
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import datetime
import json

Base = sqlalchemy.ext.declarative.declarative_base()

def dump_item_to_list(item):
    data = []
    for column in item.__table__.columns:
        data.append(getattr(item, column.name))
    return data

def dump_item_to_unicode_list(item):
    # None elems are left blank
    return [unicode(elem) if elem else u'' for elem in dump_item_to_list(item)]


class ToListMixin():
    def to_list(self):
        return dump_item_to_list(self)

    def to_unicode_list(self):
        return dump_item_to_unicode_list(self)

class SteamApp(Base, ToListMixin):
    __tablename__ = 'steam_apps'

    app_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    time_to_100 = sqlalchemy.Column(sqlalchemy.Float)
    total_points = sqlalchemy.Column(sqlalchemy.Float)
    points_per_time = sqlalchemy.Column(sqlalchemy.Float)
    num_players = sqlalchemy.Column(sqlalchemy.Integer)
    num_players_to_100 = sqlalchemy.Column(sqlalchemy.Integer)
    percentage_of_players_to_100 = sqlalchemy.Column(sqlalchemy.Float)
    astats_last_updated = sqlalchemy.Column(sqlalchemy.DateTime)
    recent_steam_rating = sqlalchemy.Column(sqlalchemy.Integer)
    overall_steam_rating = sqlalchemy.Column(sqlalchemy.Integer)
    steampowered_last_updated = sqlalchemy.Column(sqlalchemy.DateTime)


class User(Base, ToListMixin):
    __tablename__ = 'users'

    steam_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    last_updated = sqlalchemy.Column(sqlalchemy.DateTime)


class OwnedApp(Base, ToListMixin):
    __tablename__ = 'owned_apps'

    steam_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.steam_id', primary_key=True))
    app_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('steam_apps.app_id'), primary_key=True)
    number_achieved = sqlalchemy.Column(sqlalchemy.Integer)
    percentage_achieved = sqlalchemy.Column(sqlalchemy.Integer)
    last_updated = sqlalchemy.Column(sqlalchemy.DateTime)


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
        app = SteamApp(app_id=atats_app_item.get('app_id'),
                       title=atats_app_item.get('title'),
                       time_to_100=atats_app_item.get('time_to_100'),
                       total_points=atats_app_item.get('total_points'),
                       points_per_time=points_per_time,
                       num_players=atats_app_item.get('num_players'),
                       num_players_to_100=atats_app_item.get('num_players_to_100'),
                       percentage_of_players_to_100=percentage_to_hundo,
                       astats_last_updated=datetime.datetime.now(),
                       )
        self.session.merge(app)

    def store_ownership(self, owned_app_item):
        app = SteamApp(app_id=owned_app_item.get('app_id'))
        self.session.merge(app)
        user = User(steam_id=owned_app_item.get('owner_id'), last_updated=datetime.datetime.now())
        self.session.merge(user)
        owned_app = OwnedApp(steam_id=owned_app_item.get('owner_id'),
                             app_id=owned_app_item.get('app_id'),
                             number_achieved=owned_app_item.get('number_achieved'),
                             percentage_achieved=owned_app_item.get('percentage_achieved'),
                             last_updated=datetime.datetime.now()
                             )
        self.session.merge(owned_app)


    def store_app_id(self, app_item):
        app = SteamApp(id=app_item.get('app_id'))
        self.session.merge(app)

    def get_all_app_ids(self):
        ids = [id for id in self.session.query(SteamApp.app_id)]
        return ids

    def get_app_ids_for_unknown_points(self):
        ids = [id for (id,) in self.session.query(SteamApp.app_id)
            .filter(SteamApp.total_points == None)]
        return ids

    def get_app_ids_for_apps_with_points(self):
        ids = [id for (id,) in self.session.query(SteamApp.app_id)
            .filter(SteamApp.total_points > None)]
        return ids

    def get_app_ids_sorted_by_points_per_time(self):
        ids = [id for (id,) in self.session.query(SteamApp.app_id)
            .order_by(SteamApp.points_per_time)]
        return ids

    def get_owned_app_ids(self, owner_id):
        ids = [id for (id,) in self.session.query(OwnedApp.app_id)
            .filter(OwnedApp.steam_id == owner_id)]
        return ids

    def get_owned_app_info(self, owner_id, order_by=None):
        query = self.session.query(SteamApp)\
            .filter(SteamApp.app_id == OwnedApp.app_id)\
            .filter(OwnedApp.steam_id == owner_id)
        if order_by:
            query.order_by(order_by)
        return query.all()

    def get_all_apps_info(self, order_by=None):
        query = self.session.query(SteamApp)
        if order_by:
            query.order_by(order_by)
        return query.all()
