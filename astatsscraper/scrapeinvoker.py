from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.ownedgamesspider
import spiders.steamappspider


def scrape_game_ownership(steam_id):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.ownedgamesspider.OwnedGamesSpider, steam_id)
    process.start()


def scrape_steam_app(app_id):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.steamappspider.SteamAppSpider, app_id)
    process.start()
