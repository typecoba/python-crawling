# -*- coding: utf-8 -*-
import scrapy
import re
from ecommerce.items import EcommerceItem

class GmarketSpider(scrapy.Spider):
    name = 'gmarket'
    # allowed_domains = ['www.gmarket.co.kr']
    # start_urls = ['https://corners.gmarket.co.kr/Bestsellers/']
    '''
    카테고리->서브카테고리->페이지 
 
    '''

    # 젤첨에 실행되는 함수
    def start_requests(self):
        yield scrapy.Request(url='http://corners.gmarket.co.kr/Bestsellers', callback=self.parseMain)




    def parseMain(self, response):
        categoryLinks = response.css("div.gbest-cate ul.by-group li a::attr(href)").getall()
        categoryNames = response.css("div.gbest-cate ul.by-group li a::text").getall()

        # category depth.1 - all
        print("category depth.1")
        for idx, link in enumerate(categoryLinks):
            yield scrapy.Request(url="http://corners.gmarket.co.kr" + link, callback=self.parseItem, dont_filter=True, # 중복url해재
                                 meta={'mainCategoryName': categoryNames[idx], 'subCategoryName': 'ALL'})
        # category depth.2 - sub
        print("category depth.2")
        for idx, link in enumerate(categoryLinks):
            yield scrapy.Request(url="http://corners.gmarket.co.kr" + link, callback=self.parseCategory2, dont_filter=True,
                                 meta={'mainCategoryName': categoryNames[idx]})



    def parseCategory2(self, response):
        subCategoryLinks = response.css("div.cate-l .navi.group ul li a::attr(href)").getall()
        subCategoryNames = response.css("div.cate-l .navi.group ul li a::text").getall()
        # print(response.meta['mainCategoryName'], "subcategorynames",subCategoryNames)

        for idx, link in enumerate(subCategoryLinks):
            yield scrapy.Request(url='http://corners.gmarket.co.kr'+link, callback=self.parseItem,
                                 meta={'mainCategoryName':response.meta['mainCategoryName'],'subCategoryName':subCategoryNames[idx]})


    def parseItem(self, response):
        items = response.css("div.best-list")[1]  # 객체로 저장

        for idx, item in enumerate(items.css("ul li")):
            itemObj = EcommerceItem()

            rank = idx + 1
            title = item.css("a.itemname::text").get()
            oriPrice = item.css("div.o-price::text").get()
            disPrice = item.css("div.s-price strong span span::text").get()
            discountPercent = item.css("div.s-price em::text").get()

            # 전처리
            if oriPrice == None:
                oriPrice = disPrice
            oriPrice = re.sub(",|원", "", oriPrice)
            disPrice = re.sub(",|원", "", disPrice)
            if discountPercent == None:
                discountPercent = '0'
            else:
                discountPercent = discountPercent.replace("%", "")

            # item객체담기
            itemObj['mainCategoryName'] = response.meta["mainCategoryName"]
            itemObj['subCategoryName'] = response.meta["subCategoryName"]
            itemObj['rank'] = rank
            itemObj['title'] = title
            itemObj['oriPrice'] = oriPrice
            itemObj['disPrice'] = disPrice
            itemObj['discountPercent'] = discountPercent

            # export시 필드순서 유지하려면...
            # settings.py -> FEED_EXPORT_FIELDS = ['','','']

            # print(response.meta['mainCategoryName'], response.meta['subCategoryName'], rank, title, oriPrice, disPrice, discountPercent)
            yield itemObj
