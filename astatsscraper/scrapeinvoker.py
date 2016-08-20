from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.ownedgamesspider
import spiders.steamappspider
import spiders.allappidsspider
import spiders.steampoweredapppagespider
import persistence


def scrape_app_ownership(steam_id):
    """Scrapes all games owned by a user and stores ownership info in the database via pipeline. Note this will
    not scrape detailed game information, just what can be found on a users ownership page.

    Args:
        steam_id (str | int): steam id of the user to scrape ownership for.
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.ownedgamesspider.OwnedGameIdsSpider, steam_id)
    process.start()


def scrape_steam_apps(app_ids):
    """Scrape detailed information about a single or multiple steam apps.

    Args:
        app_ids (str | int | List[str] | List[int]): one or more app ids to scrape.
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.steamappspider.SteamAppSpider, app_ids)
    process.start()


def scrape_owned_apps(steam_id):
    """Scrapes all owned games for a user as reported by querying the database.

    Args:
        steam_id (str | int): steam id of the user to scrape ownership for.
    """
    with persistence.Persistor() as persistor:
        scrape_steam_apps(persistor.get_owned_app_ids(steam_id))


def scrape_apps_with_unknown_points():
    """Scrapes all games in database with unknown point values"""
    with persistence.Persistor() as persistor:
        scrape_steam_apps(persistor.get_app_ids_for_unknown_points())


def scrape_all_game_ids():
    """Scrapes all game ids from astats."""
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.allappidsspider.AllAppIdsSpider)
    process.start()


def scrape_steam_powered_app_pages(app_ids):
    """Scrapes a steampowered.com for information.

    Args:
         app_ids (str | int | List[str] | List[int]): one or more app ids to scrape.
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders.steampoweredapppagespider.SteamPoweredAppPageSpider, app_ids)
    process.start()


def scrape_steam_powered_owned_app_pages(steam_id):
    with persistence.Persistor() as persistor:
        scrape_steam_powered_app_pages(persistor.get_owned_app_ids(steam_id))
