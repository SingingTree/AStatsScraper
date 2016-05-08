SPIDER_MODULES = ['astatsscraper.spiders']
NEWSPIDER_MODULE = 'astatsscraper.spiders'

ITEM_PIPELINES = {
    'astatsscraper.pipelines.SteamAppPipeline': 0,
    'astatsscraper.pipelines.AppOwnerPipeline': 3
}

DOWNLOAD_DELAY = 0.25 # 250 ms of delay
