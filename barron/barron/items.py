# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BarronItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    subtitle = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
    body = scrapy.Field()
    category = scrapy.Field()
    company = scrapy.Field()
    year = scrapy.Field()
