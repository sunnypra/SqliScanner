import scrapy
from scrapy.item import Item, Field


class Website(Item): 
    name = Field() 
    url = Field() 
    description = Field()
