# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CulturefrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    word_name = scrapy.Field()
    synonyme = scrapy.Field()
    domain = scrapy.Field()
    definition = scrapy.Field()
    note = scrapy.Field()
    voir_aussi = scrapy.Field()
    equivalent = scrapy.Field()
    journal_official_du = scrapy.Field()
    source = scrapy.Field()
    pass
