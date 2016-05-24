import scrapy
import astatsscraper.parsing
import astatsscraper.pipelines

class AllAppsSpider(scrapy.Spider):
    name = 'AllAppsSpider'
    pipeline = []
    start_urls = 'http://astats.astats.nl/astats/Steam_Games.php?DisplayType=All'


    def parse(self, response):
        return astatsscraper.parsing.parse_search_page(response)