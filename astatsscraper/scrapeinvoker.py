from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.ownedgamesspider
import spiders.steamappspider
import persistence


def scrape_game_ownership(steam_id):
    """Scrapes owned games owned by a user and stores ownership info in the database via pipeline. Note this will
    not scrape all game information, just the app_id."""
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.ownedgamesspider.OwnedGamesSpider, steam_id)
    process.start()


def scrape_steam_apps(app_id):
    """Scrape detailed infomation about a steam app."""
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.steamappspider.SteamAppSpider, app_id)
    process.start()


def scrape_owned_games(steam_id):
    """Scrapes all owned games for a user as reported by querying the database."""
    with persistence.Persistor() as persistor:
        scrape_steam_apps(persistor.get_owned_app_ids(steam_id))

