SPIDER_MODULES = ['astatsscraper.spiders']
NEWSPIDER_MODULE = 'astatsscraper.spiders'
DEFAULT_ITEM_CLASS = 'astatsscraper.items.SteamAppItem'

ITEM_PIPELINES = {
    'astatsscraper.pipelines.SteamAppPipeline': 0,
    'astatsscraper.pipelines.AppOwnerPipeline': 3
}
