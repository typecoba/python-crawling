# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from urllib.parse import urlparse

# IMAGES_URLS_FIELD = 'image_urls'
# IMAGES_RESULT_FIELD = 'images'

class CyworldPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for idx, url in enumerate(item['image_urls']):
            request = scrapy.Request(url)
            request.meta['image_name'] = item['image_names'][idx]
            request.meta['file_no'] = idx+1
            request.meta['post_no'] = item['no']
            yield request

    def file_path(self, request, response=None, info=None):
        return '/{post_no}.{file_no}.{name}'.format(post_no=request.meta['post_no'], file_no=request.meta['file_no'] ,name=request.meta['image_name'])

    def item_complete(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class FilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for idx, url in enumerate(item['file_urls']):
            request = scrapy.Request(url)
            request.meta['file_name'] = item['file_names'][idx]
            request.meta['file_no'] = idx + 1
            request.meta['post_no'] = item['no']
            yield request

    def file_path(self, request, response=None, info=None):
        return '/{post_no}.{file_no}.{name}'.format(post_no=request.meta['post_no'], file_no=request.meta['file_no'] ,name=request.meta['file_name'])

    def item_complete(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no images")
        item['file_paths'] = file_paths
        return item