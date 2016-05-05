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

    def __init__(self, app_id, *args, **kwargs):
        super(SteamAppSpider, self).__init__(*args, **kwargs)

        self.start_urls = [A_STATS_APP_URL_BASE + str(app_id)]

    def parse(self, response):
        return astatsscraper.parsing.parse_app_page(response)

