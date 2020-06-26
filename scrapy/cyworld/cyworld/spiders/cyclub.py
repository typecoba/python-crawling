# -*- coding: utf-8 -*-
import scrapy
import re
from cyworld.items import CyclubPostItem


class CyclubSpider(scrapy.Spider):
    name = 'cyclub'
    host = 'http://club.cyworld.com'

    # allowed_domains = ['club.cyworld.com']
    # start_urls = ['http://club.cyworld.com/']

    club_id = 53046142


    # 게시판 목록
    # startUrl = 'http://club.cyworld.com/ClubV1/Home.cy/53046142'

    # 전체글보기 게시판
    startUrl = 'http://club.cyworld.com/club/board/general/AllListNormal.asp?cpage={cpage}&club_id=53046142&board_no=0&board_type=1&list_type=0&show_type=5&headtag_seq=&search_type=&search_keyword=&search_block=1'

    # 전체사진보기 게시판
    # startUrl = 'http://club.cyworld.com/club/board/image/AllListAlbum.asp?cpage={cpage}&club_id=53046142&board_no=0&board_type=2&list_type=0&show_type=5&search_type=&search_keyword=&search_block=0&Scpage='

    # 글
    # startUrl = 'http://club.cyworld.com/Club/Board/General/View.asp?club_id=53046142&board_no=135&search_type=&search_keyword=&item_seq=55872919&cpage=2&search_block=1&Scpage=1&board_type=1&&list_type=0&show_type=5&openboard_flag=1&headtag_seq=&club_auth=6'
    # startUrl = 'http://club.cyworld.com/Club/Board/General/View.asp?club_id=53046142&board_no=135&search_type=&search_keyword=&item_seq=55863924&cpage=2&search_block=1&Scpage=1&board_type=1&&list_type=0&show_type=5&openboard_flag=1&headtag_seq=&club_auth=6'

    # 댓글
    # commentUrl = 'http://club.cyworld.com/club/board/common/CommentList.asp?club_id=53046142&board_type=1&board_no=135&item_seq=55863924'

    # 사진post
    # startUrl = 'http://club.cyworld.com/club/board/image/View.asp?club_id=53046142&board_no=2&search_type=&search_keyword=&item_seq=328582311&cpage=1&search_block=0&Scpage=1&board_type=2&list_type=0&show_type=5'

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection':'keep-alive',
        'Host':'club.cyworld.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept-Encoding':'*/*',
        'Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1'
    }
    cookies = {
        'cookieinfouser': '7fcdfdb1a7f4df5f43e6630ec517a6f4e3d19edd1446ebd616856670e8a39448d5a3983a9d0e43cea78d72ace73e8490a438c4b2708cad50d1a18080d58356cb1dca69a2f16673f53decbaae08272977abe52527436046705cf428a9a638f2c4d59b6de7f3015e782b9bb7de4153c5b42f853a4824b753bd5a4aff3c014200fd956e87503f3ff65f09928376b4607bd46a9fa016764233e728fc525047140b332ce433c4245837cf646cc9fd5b8447f9'
    }

    def start_requests(self):

        # 전체글 게시판
        for num in range(63) :
            yield scrapy.Request(url=self.startUrl.format(cpage=num+1),
                             method='GET',
                             callback=self.parse_board,
                             headers=self.headers,
                             cookies=self.cookies,
                             meta={})

        # 전체 사진 게시판
        # for num in range(6):
        #     yield scrapy.Request(url=self.startUrl.format(cpage=num+1),
        #                          method='GET',
        #                          callback=self.parse_image_board,
        #                          headers=self.headers,
        #                          cookies=self.cookies,
        #                          meta={'no':'test'})

    # 전체 사진보기
    def parse_image_board(self, response):
        # print(response.text)
        postUrls = response.css('#wrap_cmn_board .wrap_p_list > ul > li.mdl_p_list .thumbbox a::attr(href)').getall()
        postUrls = list(map(lambda x: self.host + "/club/board/image/" + re.sub("javascript:location.href='|';return false;",'',x), postUrls))
        print(postUrls)

        for idx, url in enumerate(postUrls):
            # if idx > 2 : continue
            yield scrapy.Request(url=url,
                                 method='GET',
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 callback=self.parse_post,
                                 meta={'no':idx}
                                 )



    # 전체 글 보기
    def parse_board(self, response):
        # print(response.text)

        # post urls
        postNums = response.css('#wrap_cmn_board table > tbody > tr > td.col_num .wrap_numbox::text').getall()
        postNums = list(filter(lambda x: x!='', map(lambda x: x.strip(), postNums) )) # 전처리
        postUrls = response.css('#wrap_cmn_board table > tbody > tr > td.col_title a::attr(onclick)').getall()
        postUrls = list(map(lambda x: self.host + re.sub("javascript:location.href='|';return false;",'',x) ,postUrls))
        # print(postUrls)
        # print(postNums)

        # pass
        for idx, url in enumerate(postUrls):
            # if idx > 2 : continue
            yield scrapy.Request(url=url,
                                 method='GET',
                                 callback=self.parse_post,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 meta={'no':postNums[idx].strip()}
                                 )


    def parse_post(self, response):
        item = CyclubPostItem()

        no = response.meta['no']
        category = response.css('#boardTitle::text').get()
        title = response.css('.wrap_contentview .wrapTitle h4::text').get()
        writer = response.css('.wrap_contentview .box_posting_info .fl .nameui::text').get()
        date = response.css('.wrap_contentview .box_posting_info .fl .dateinfo::text').get()
        view = response.css('.wrap_contentview .box_posting_info .countinfo em::text').get()
        article = response.css('#main_content ::text').getall()
        data_types = response.css('.wrap_contentview .file_list li img::attr(src)').getall()
        data_names = response.css('.wrap_contentview .file_list li a::text').getall()
        data_urls = response.css('.wrap_contentview .file_list li a::attr(href)').getall()

        # 전처리
        article = re.sub('^P {.*}|\xa0|\u200e', '', '\n'.join(article)).strip()
        data_names = list(map(lambda x: x.strip(), data_names))
        data_urls = list(map(lambda x: self.host + x, data_urls))
        title = re.sub('\xa0|\u200e', '', title.strip())

        # 첨부파일 구분
        image_names = []
        image_urls = []
        file_names = []
        file_urls = []
        for idx, type in enumerate(data_types) :
            if type.find('ico_attach_img.gif') != -1 : #이미지인경우
                image_names.append(data_names[idx])
                image_urls.append(data_urls[idx])
            else : # 파일인 경우
                file_names.append(data_names[idx])
                file_urls.append(data_urls[idx])

        # 사진게시판의 경우
        code = response.css('.box_posting_info::attr(id)').get()
        image_names.append('{}_{}_{}.jpg'.format(date[0:10],title,code[5:]))
        image_urls.append(response.css('.photo-detail img::attr(src)').get())

        # item
        item['no'] = no
        item['category'] = category
        item['title'] = title
        item['writer'] = writer
        item['date'] = date
        item['view'] = view
        item['image_names'] = image_names
        item['image_urls'] = image_urls
        item['file_names'] = file_names
        item['file_urls'] = file_urls
        item['article'] = article

        # print(item)
        # item['comments'] = ''
        # yield item


        # 댓글 url정보 추출
        # 있는지 없는지 호출해야 알수있음..
        board_type = response.css('#board_item #board_type::attr(value)').get()
        board_no = response.css('#board_item #board_no::attr(value)').get()
        item_seq = response.css('#board_item #item_seq::attr(value)').get()
        comment_url = 'http://club.cyworld.com/club/board/common/CommentList.asp?' \
                      'club_id={club_id}&board_type={board_type}&board_no={board_no}&item_seq={item_seq}'\
                      .format(club_id=self.club_id, board_type=board_type, board_no=board_no, item_seq=item_seq)
        meta = {'item' : item} # item정보 넘기기


        yield scrapy.Request(url=comment_url,
                             callback=self.parse_comment,
                             headers=self.headers,
                             cookies=self.cookies,
                             meta=meta)



    def parse_comment(self, response):
        # 댓글없는경우?
        # if response.text=='' :
        #     item = response.meta['item']
        #     item['comments'] = ''
        #     yield item
        #     pass



        # tr .new_re 무시
        # tr .re_reply 와 분기해야함
        comments = response.css('.box_reply > table > tbody > tr')
        # comment_item = CyclubCommentItem()
        comments_str = ''

        for idx, row in enumerate(comments):
            type = row.xpath('@class').get()
            if type==None :
                comment_writer = row.css('.uname .nameui::text').get()
                comment_article = row.css('.title .obj_rslt::text').get()
                comment_date = row.css('.date::text').get()
            elif type=='re_reply': # 대댓글인경우
                comment_writer = row.css('table > tbody > tr td.uname .nameui::text').get()
                comment_article = row.css('table > tbody > tr td.title .obj_rslt::text').get()
                comment_date = row.css('table > tbody > tr td.date::text').get()
            elif type=='new_re':
                continue

            # comment_item['comment_writer'] = comment_writer
            # comment_item['comment_article'] = comment_article
            # comment_item['comment_date'] = comment_date

            comments_str = comments_str + '{0} {1} {2}\n'.format(comment_writer,comment_article,comment_date)


        # 여기에 item을 어떻게 붙이지???
        item = response.meta['item']
        item['comments'] = comments_str

        yield item
