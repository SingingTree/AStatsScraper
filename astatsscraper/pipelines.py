from .persistence import *


class AppIdOnlyPipeline(object):
    def process_item(self, item, spider):
        if self.__class__ in spider.pipeline:
            with persistence.Persistor() as persistor:
                persistor.store_app_id(item)
            return item
        else:
            return item


class AppOwnerPipeline(object):
    def process_item(self, item, spider):
        if self.__class__ in spider.pipeline:
            with persistence.Persistor() as persistor:
                persistor.store_ownership(item)
            return item
        else:
            return item


class SteamAppPipeline(object):
    def process_item(self, item, spider):
        if self.__class__ in spider.pipeline:
            with persistence.Persistor() as persistor:
                persistor.store_astats_app(item)
            return item
        else:
            return item


class SteamPoweredAppPagePipeline(object):
    def process_item(self, item, spider):
        if self.__class__ in spider.pipeline:
            with persistence.Persistor() as persistor:
                persistor.store_steampowered_app(item)
            return item
        else:
            return item
