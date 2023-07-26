# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from collections import OrderedDict


class CrawlCafefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewItem(scrapy.Item):
    
    Category = scrapy.Field()
    Created = scrapy.Field()
    Link = scrapy.Field()
    Title = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(NewItem, self).__init__(*args, **kwargs)
        self._values = OrderedDict()

        for key in self.fields:
            self._values[key] = None
