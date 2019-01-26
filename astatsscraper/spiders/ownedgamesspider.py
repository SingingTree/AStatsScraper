import scrapy
import astatsscraper.parsing
import astatsscraper.pipelines

# Info on spiders with args:
# http://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments

A_STATS_OWNED_GAMES_URL_BASE = 'https://astats.astats.nl/astats/User_Games.php?SPL=0&CTO=0&Limit=0&ToPlay=0&PerfectOnly=0&Hidden=0&AchievementsOnly=0&DisplayType=2&GTF=0&SteamID64='


class OwnedGameIdsSpider(scrapy.Spider):
    name = 'OwnedGamesSpider'
    pipeline = [astatsscraper.pipelines.AppOwnerPipeline]

    def __init__(self, steam_id, *args, **kwargs):
        super(OwnedGameIdsSpider, self).__init__(*args, **kwargs)

        self.start_urls = [A_STATS_OWNED_GAMES_URL_BASE + str(steam_id)]

    def parse(self, response):
        return astatsscraper.parsing.parse_owned_games_for_apps(response)
