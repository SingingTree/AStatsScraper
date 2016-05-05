from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.ownedgamesspider

def scrape_games_owned_by_user(steam_id):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.ownedgamesspider.OwnedGamesSpider, steam_id)
    process.start()
