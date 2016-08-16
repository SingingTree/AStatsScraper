import scrapy
import astatsscraper.parsing
import astatsscraper.pipelines

# Info on spiders with args:
# http://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments

STEAM_POWERED_APP_URL_BASE = 'http://store.steampowered.com/app/'


class SteamPoweredAppPageSpider(scrapy.Spider):
    name = 'SteamAppSpider'
    pipeline = [astatsscraper.pipelines.SteamPoweredAppPagePipeline]

    def __init__(self, app_ids, steam_id=None, *args, **kwargs):
        super(SteamPoweredAppPageSpider, self).__init__(*args, **kwargs)
        if isinstance(app_ids, list):
            self.start_urls = [STEAM_POWERED_APP_URL_BASE + str(id) for id in app_ids]
        else:
            self.start_urls = [STEAM_POWERED_APP_URL_BASE + str(app_ids)]

    def parse(self, response):
        return astatsscraper.parsing.parse_steam_powered_app_page(response)