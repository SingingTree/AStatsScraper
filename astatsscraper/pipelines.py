import persistence

class SteamAppPipeline(object):
    def process_item(self, item, spider):
        if self.__class__ in spider.pipeline:
            with persistence.Persistor() as persistor:
                if item.get('owner'):
                    print("item has owner")
                persistor.store_app(item)
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