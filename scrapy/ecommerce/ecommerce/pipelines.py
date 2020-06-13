# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class EcommercePipeline(object):
    def process_item(self, item, spider):

        if int(item['price']) > 10000:
            return item
        else:
            raise DropItem("dropItem",item) #item을 없애 버리기때문에 다른처리를 더이상 안하게 됨