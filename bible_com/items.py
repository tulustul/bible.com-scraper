# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Book(scrapy.Item):
    translation = scrapy.Field()
    fullname = scrapy.Field()
    shortname = scrapy.Field()


class Verse(scrapy.Item):
    translation = scrapy.Field()
    book = scrapy.Field()
    chapter = scrapy.Field()
    verse = scrapy.Field()
    text = scrapy.Field()
