import scrapy
import astatsscraper.parsing
import astatsscraper.pipelines


class AllAppIdsSpider(scrapy.Spider):
    name = 'AllAppsSpider'
    pipeline = [astatsscraper.pipelines.AppIdOnlyPipeline]
    start_urls = ['https://astats.astats.nl/astats/Steam_Games.php?DisplayType=All']

    def parse(self, response):
        return astatsscraper.parsing.parse_search_result_for_apps_recursive(response)
