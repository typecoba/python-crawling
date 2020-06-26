# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CyclubPostItem(scrapy.Item):
    # define the fields for your item here like:
    columns = ['no','category','title','writer','date','view','image_names','image_urls','file_names','file_urls','article','comments']

    no = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    writer = scrapy.Field()
    date = scrapy.Field()
    view = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_names = scrapy.Field()
    files = scrapy.Field()
    file_urls = scrapy.Field()
    file_names = scrapy.Field()
    article = scrapy.Field()
    comments = scrapy.Field()

    def get_columns(self):
        return self.columns
