# -*- coding: utf-8 -*-
import scrapy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    # allowed_domains = ['www.instagram.com']
    # start_urls = ['http://www.instagram.com/']

    def start_requests(self):
        # 1. 로그인 정보 cookie로 넘겨 profile, post, tag, explore 정보 접근하기
        # 2. 데이터 export, db insert
        # 3. 맥락
        urlProfile = 'https://www.instagram.com/typecoba/?__a=1' # profile
        urlPost = 'https://www.instagram.com/p/CA0fqWxl8ny/?__a=1' # post
        urlTag = 'https://www.instagram.com/explore/tags/펭수/?__a=1' # tag

        # private api에서 추출한 url
        # header,cookie 설정필요(로그인, 기기, 앱)
        urlPrivate = 'https://i.instagram.com/api/v1/users/253147072/info' # private cm_id


        # cookie
        # 로그인 후 생성된 쿠키 유지해야함
        cookies = {
            'urlgen':'"{\"112.220.194.91\": 3786}:1jkkkG:4xCTxGA06oUpL0ejaKlg8Jw6HZ8"',
            'shbts':'1592210732.200599',
            'sessionid':'253147072%3APVKHHpso4tBliC%3A8',
            'csrftoken':'Dyct7yf3WRuVxFf51uNQpHrCvgtZ3LUU',
            'shbid':'11605',
            'mid':'Xrn-3AAEAAEP94fesPijHdSLtDKA',
            'ds_user_id':'253147072',
            'ig_did':'1435645E-ADB5-404F-92FA-8485BB62A2E0'
        }
        # header
        # user agent에 모바일 + 앱 정보가 필요한경우 있음
        headers = {
            'Authority': 'www.instagram.com',
            'Method': 'GET',
            'Cache-control': 'no-cache',
            'Pragma': 'no-cache',
            'Upgrade-insecure-requests': '1',
            'Accept-language': 'en',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920)',
            'Content-Type': 'application/json'
        }

        # 호출 limit는 test가 필요한 부분이라 test용 계정하나 만들어서 시험해볼 필요성 있음
        # 근데이건 람다를 통해 어느정도 해결..


        yield scrapy.Request(url=urlPrivate, method='GET',
                             headers= headers,
                             cookies= cookies,
                             callback=self.parse,
                             meta={})

    def parse(self, response):
        print(response.text)