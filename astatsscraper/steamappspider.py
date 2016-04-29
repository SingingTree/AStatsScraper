import scrapy
import parsing

# Info on spiders with args:
# http://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments

A_STATS_APP_URL_BASE = 'http://astats.astats.nl/astats/Steam_Game_Info.php?AppID='


class SteamAppSpider(scrapy.Spider):
    name = 'SteamAppSpider'

    def __init__(self, app_id, *args, **kwargs):
        super(SteamAppSpider, self).__init__(*args, **kwargs)

        self.start_urls = [A_STATS_APP_URL_BASE + str(app_id)]

    def parse(self, response):
        return parsing.parse_app_page(response)

