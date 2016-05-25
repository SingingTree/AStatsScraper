import scrapy
import astatsscraper.parsing
import astatsscraper.pipelines


class AllAppsSpider(scrapy.Spider):
    name = 'AllAppsSpider'
    pipeline = []
    start_urls = ['http://astats.astats.nl/astats/Steam_Games.php?DisplayType=All']

    def parse(self, response):
        #itertools.chain generators for each page, use them to read app data
        next_page = astatsscraper.parsing.parse_search_result_for_next_page(response)
        return astatsscraper.parsing.parse_search_result_for_apps(response)