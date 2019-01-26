import scrapy
import astatsscraper.parsing
import astatsscraper.pipelines

# Info on spiders with args:
# http://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments

STEAM_POWERED_APP_URL_BASE = 'https://store.steampowered.com/app/'


class SteamPoweredAppPageSpider(scrapy.Spider):
    name = 'SteamPoweredAppSpider'
    pipeline = [astatsscraper.pipelines.SteamPoweredAppPagePipeline]

    def __init__(self, app_ids, steam_id=None, *args, **kwargs):
        super(SteamPoweredAppPageSpider, self).__init__(*args, **kwargs)
        if isinstance(app_ids, list):
            self.start_urls = [STEAM_POWERED_APP_URL_BASE + str(id) for id in app_ids]
        else:
            self.start_urls = [STEAM_POWERED_APP_URL_BASE + str(app_ids)]

    # Set birthtime to pass age gates
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'birthtime': '378644401'}, callback=self.parse)

    def parse(self, response):
        return astatsscraper.parsing.parse_steam_powered_app_page(response)