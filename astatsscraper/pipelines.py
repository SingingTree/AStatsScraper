import persistence

class SteamAppPipeline(object):
    def process_item(self, item, spider):
        with persistence.Persistor() as persistor:
            persistor.store_app(item)
            return item