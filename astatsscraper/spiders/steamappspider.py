import scrapy
from scrapy.settings.default_settings import ITEM_PIPELINES
import astatsscraper.parsing
import astatsscraper.pipelines

# Info on spiders with args:
# http://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments

A_STATS_APP_URL_BASE = 'http://astats.astats.nl/astats/Steam_Game_Info.php?AppID='


class SteamAppSpider(scrapy.Spider):
    name = 'SteamAppSpider'
    pipeline = [astatsscraper.pipelines.SteamAppPipeline]

    def __init__(self, app_ids, steam_id=None, *args, **kwargs):
        super(SteamAppSpider, self).__init__(*args, **kwargs)
        if isinstance(app_ids, list):
            self.start_urls = [A_STATS_APP_URL_BASE + str(id) for id in app_ids]
        else:
            self.start_urls = [A_STATS_APP_URL_BASE + str(app_ids)]

    def parse(self, response):
        return astatsscraper.parsing.parse_app_page(response)

