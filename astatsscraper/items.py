import scrapy


class AstatsSteamappItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    time_to_100 = scrapy.Field()
    total_points = scrapy.Field()
    num_players = scrapy.Field()
    num_players_to_100 = scrapy.Field()


class SteampoweredSteamappItem(scrapy.Item):
    id = scrapy.Field()
    recent_rating = scrapy.Field()
    overall_rating = scrapy.Field()


class OwnedAppItem(scrapy.Item):
    owner_id = scrapy.Field()
    app_id = scrapy.Field()
    number_achieved = scrapy.Field()
    percentage_achieved = scrapy.Field()
