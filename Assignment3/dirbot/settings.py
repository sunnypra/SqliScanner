# Scrapy settings for dirbot1 project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1}
