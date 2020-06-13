# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class NaveropenapiPipeline(object):
    def process_item(self, item, spider):
        item['title'] = re.sub("(<b>|</b>)", "",item["title"])
        return item
