# -*- coding: utf-8 -*-
import scrapy
import re
from cyworld.items import CyclubPostItem
from cyworld.items import CyclubCommentItem



class CyclubSpider(scrapy.Spider):
    name = 'cyclub'

    # allowed_domains = ['club.cyworld.com']
    # start_urls = ['http://club.cyworld.com/']

    club_id = 53046142


    # 게시판 목록
    # startUrl = 'http://club.cyworld.com/ClubV1/Home.cy/53046142'

    # 전체목록
    # startUrl = 'http://club.cyworld.com/club/board/general/AllListNormal.asp?cpage=1&club_id=53046142&board_no=0&board_type=1&list_type=0&show_type=5&headtag_seq=&search_type=&search_keyword=&search_block=1'

    # 글
    startUrl = 'http://club.cyworld.com/Club/Board/General/View.asp?club_id=53046142&board_no=135&search_type=&search_keyword=&item_seq=55872919&cpage=2&search_block=1&Scpage=1&board_type=1&&list_type=0&show_type=5&openboard_flag=1&headtag_seq=&club_auth=6'

    # 댓글
    # commentUrl = 'http://club.cyworld.com/club/board/common/CommentList.asp?club_id=53046142&board_type=1&board_no=135&item_seq=55863924'

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
        'cookieinfouser': '7fcdfdb1a7f4df5f43e6630ec517a6f4e3d19edd1446ebd616856670e8a39448d7c48e48516fd31b4b22eea6f48be6f4a74de775a883cf918eef1c97a30f35a90f3a20e2e8d3ecbba933b4768e96f7c263060b6a82881e41c6a6a5c2ca02736bfe6b7455ac96ce8f43c4602dee141b14298eaa677c228a715b6bc426599b8ad96d1fd5550c35fed0af1ae53f666d0ea2a7239cc2528bc3f83adc8d796f12aa8b1205b03cc77480d41cff3213336dd6ce'
    }
    meta = {'no':'test', 'image_name':'image_name.jpg'}

    def start_requests(self):
        yield scrapy.Request(url=self.startUrl,
                             method='GET',
                             callback=self.parse_post,
                             headers=self.headers,
                             cookies=self.cookies,
                             meta=self.meta)

    def parse_board_list(self, response):
        # board_group_name
        # board_name
        # board_num
        pass

    def parse_list(self, response):
        # print(response.text)
        # no.
        # title
        # writer
        # date
        # view
        pass

    def parse_post(self, response):
        item = CyclubPostItem()

        no = response.meta['no']
        category = response.css('#boardTitle::text').get()
        title = response.css('.wrap_contentview .wrapTitle h4::text').get()
        writer = response.css('.wrap_contentview .box_posting_info .fl .nameui::text').get()
        date = response.css('.wrap_contentview .box_posting_info .fl .dateinfo::text').get()
        view = response.css('.wrap_contentview .box_posting_info .countinfo em::text').get()
        article = response.css('#main_content p').getall()
        data_types = response.css('.wrap_contentview .file_list li img::attr(src)').getall()
        data_names = response.css('.wrap_contentview .file_list li a::text').getall()
        data_urls = response.css('.wrap_contentview .file_list li a::attr(href)').getall()

        # 전처리
        article = re.sub('<p>|</p>|\xa0', '', '\n'.join(article))
        data_names = list(map(lambda x: x.strip(), data_names))
        data_urls = list(map(lambda x: 'http://club.cyworld.com' + x, data_urls))
        title = title.strip()

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
        # yield item
        board_type = response.css('#board_item #board_type::attr(value)').get()
        board_no = response.css('#board_item #board_no::attr(value)').get()
        item_seq = response.css('#board_item #item_seq::attr(value)').get()
        comment_url = 'http://club.cyworld.com/club/board/common/CommentList.asp?' \
                      'club_id={club_id}&board_type={board_type}&board_no={board_no}&item_seq={item_seq}'\
                      .format(club_id=self.club_id, board_type=board_type, board_no=board_no, item_seq=item_seq)
        print(comment_url)
        comment_meta = {}
        yield scrapy.Request(url=comment_url,
                             callback=self.parse_comment,
                             headers=self.headers,
                             cookies=self.cookies,
                             meta=comment_meta)


    def parse_comment(self, response):

        # tr .new_re 무시
        # tr .re_reply 와 분기해야함
        comments = response.css('.box_reply > table > tbody > tr')

        for idx, row in enumerate(comments):
            type = row.xpath('@class').get()
            if type==None :
                comment_writer = row.css('.uname .nameui::text').get()
                comment_article = row.css('.title .obj_rslt::text').get()
                comment_date = row.css('.date::text').get()
            elif type=='re_reply' : # 대댓글인경우
                comment_writer = row.css('table > tbody > tr td.uname .nameui::text').get()
                comment_article = row.css('table > tbody > tr td.title .obj_rslt::text').get()
                comment_date = row.css('table > tbody > tr td.date::text').get()
            elif type=='new_re' :
                continue

            print(comment_writer, comment_article, comment_date)