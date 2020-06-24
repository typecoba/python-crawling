# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CyclubPostItem(scrapy.Item):
    # define the fields for your item here like:
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

class CyclubCommentItem(scrapy.Item):
    comments = scrapy.Field()
    comment_writer = scrapy.Field()
    comment_article = scrapy.Field()
    comment_date = scrapy.Field()
