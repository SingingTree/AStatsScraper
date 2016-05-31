SPIDER_MODULES = ['astatsscraper.spiders']
NEWSPIDER_MODULE = 'astatsscraper.spiders'

ITEM_PIPELINES = {
    'astatsscraper.pipelines.SteamAppPipeline': 0,
    'astatsscraper.pipelines.AppIdOnlyPipeline': 2,
    'astatsscraper.pipelines.AppOwnerPipeline': 3
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 0,
}

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.25 # 250 ms of delay
