import scrapy

class SteamappItem(scrapy.Item):
    id  = scrapy.Field()
    title = scrapy.Field()
    time_to_100 = scrapy.Field()
    total_points = scrapy.Field()
    owner = scrapy.Field()

class OwnedAppItem(scrapy.Item):
    owner_id = scrapy.Field()
    app_id = scrapy.Field()
