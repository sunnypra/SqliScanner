# Scrapy settings for dirbot1 project

SPIDER_MODULES = ['dirbot1.spiders']
NEWSPIDER_MODULE = 'dirbot1.spiders'
DEFAULT_ITEM_CLASS = 'dirbot1.items.Website'

ITEM_PIPELINES = {'dirbot1.pipelines.FilterWordsPipeline': 1}
