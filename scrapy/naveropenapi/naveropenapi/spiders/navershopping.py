# -*- coding: utf-8 -*-
import scrapy
import json
from naveropenapi.items import NaveropenapiItem

class NavershoppingSpider(scrapy.Spider):
    name = 'navershopping'
    # allowed_domains = ['openapi.naver.com/v1/search/shop.json?query=']



    def start_requests(self):
        startUrl = 'https://openapi.naver.com/v1/search/shop.json?query='
        clientId = 'cl7k_aEwJnbYG_dh0KGf'
        clientSecret = 'v0fWt6JW2F'
        headerParams = {'X-Naver-Client-Id':clientId, 'X-Naver-Client-Secret':clientSecret}
        query='iphone'
        for idx in range(10):
            yield scrapy.Request(url=startUrl+query+'&display=100&start='+str(idx*100+1), headers=headerParams, callback=self.parse, meta={})

    def parse(self, response):
        print(response.text)
        data = json.loads(response.text) # 한글처리
        for item in data['items']:
            itemObj = NaveropenapiItem()
            itemObj['title'] = item['title']
            itemObj['link'] = item['link']
            itemObj['image'] = item['image']
            itemObj['lprice'] = item['lprice']
            itemObj['hprice'] = item['hprice']
            itemObj['mallName'] = item['mallName']
            itemObj['productId'] = item['productId']
            itemObj['productType'] = item['productType']
            yield itemObj