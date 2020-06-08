import scrapy
import json
import time
import random

class TestItem(scrapy.Item):
    id = scrapy.Field()
    reviewScore = scrapy.Field()
    writerId = scrapy.Field()
    writerProfileImageUrl = scrapy.Field()
    purchasedProductName = scrapy.Field()
    purchasedOptionContents = scrapy.Field()
    createdDate = scrapy.Field()
    best = scrapy.Field()
    repurchase = scrapy.Field()
    afterMonth = scrapy.Field()
    freeTrialReview = scrapy.Field()
    helpCount = scrapy.Field()
    help = scrapy.Field()
    contentType = scrapy.Field()
    contents = scrapy.Field()
    comments = scrapy.Field()
    resources = scrapy.Field()
    reportable = scrapy.Field()
    reportStatusCheckUrl = scrapy.Field()
    userSizeText = scrapy.Field()
    parentReviewSeq = scrapy.Field()
    highLightedContent = scrapy.Field()
    channelServiceType = scrapy.Field()
    visible = scrapy.Field()
    eventSeq = scrapy.Field()
    eventTitle = scrapy.Field()
    representResource = scrapy.Field()
    reviewScorePercent = scrapy.Field()
    pass

class Test_spider(scrapy.Spider):
    name = 'test_spider'

    # 스토어 루트
    mainUrl = 'https://smartstore.naver.com/lingerwater/products/2800118009'
    reviewUrl = 'https://smartstore.naver.com/lingerwater/products/2796364821/reviews/page.json?page=2&size=20&sortType=REVIEW_RANKING&contentType=ALL&topicCode='
    headers = {'referer': mainUrl}
    size = 30
    sortType = 'REVIEW_CREATE_DATE_DESC'
    contentsType = 'ALL'

    def start_requests(self):
        urls = [self.mainUrl]
        # 리뷰 1page
        url = 'https://smartstore.naver.com/lingerwater/products/2796364821/reviews/page.json?page={0}&size={1}&sortType={2}&contentType={3}&topicCode='.format(1, self.size, self.sortType, self.contentsType)
        # print(url)
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parseFirst)

    def parseFirst(self, response):
        # unicode로 바꾼다음 dict 변환
        jsonData = json.loads(response.body_as_unicode())
        totalPages = jsonData['htReturnValue']['pagedResult']['totalPages']

        # 이후 리뷰 페이지
        # print(totalPages)
        # totalPages = 3
        for i in range(1,totalPages+1,1):
            url = 'https://smartstore.naver.com/lingerwater/products/2796364821/reviews/page.json?page={0}&size={1}&sortType={2}&contentType={3}&topicCode='.format(i, self.size, self.sortType, self.contentsType)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parseReviewPages)
            time.sleep(random.uniform(1,2))



    def parseReviewPages(self, response):
        jsonData = json.loads(response.body_as_unicode())
        content = jsonData['htReturnValue']['pagedResult']['content']
        for i,d in enumerate(content):
            # print(i)
            item = TestItem()
            item['id'] = d['id']
            item['reviewScore'] = d['reviewScore']
            item['writerId'] = d['writerId']
            item['writerProfileImageUrl'] = d['writerProfileImageUrl']
            item['purchasedProductName'] = d['purchasedProductName']
            item['purchasedOptionContents'] = d['purchasedOptionContents']
            item['createdDate'] = d['createdDate']
            item['best'] = d['best']
            item['repurchase'] = d['repurchase']
            item['afterMonth'] = d['afterMonth']
            item['freeTrialReview'] = d['freeTrialReview']
            item['helpCount'] = d['helpCount']
            item['help'] = d['help']
            item['contentType'] = d['contentType']
            item['contents'] = d['contents']
            item['comments'] = d['comments']
            item['resources'] = d['resources']
            item['reportable'] = d['reportable']
            item['reportStatusCheckUrl'] = d['reportStatusCheckUrl']
            item['userSizeText'] = d['userSizeText']
            item['parentReviewSeq'] = d['parentReviewSeq']
            item['highLightedContent'] = d['highLightedContent']
            item['channelServiceType'] = d['channelServiceType']
            item['visible'] = d['visible']
            item['eventSeq'] = d['eventSeq']
            item['eventTitle'] = d['eventTitle']
            item['representResource'] = d['representResource']
            item['reviewScorePercent'] = d['reviewScorePercent']
            yield item