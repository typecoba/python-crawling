from itertools import count
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_request_url(url):
    try :
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        print("URL request Success")
        return soup

    except Exception as e:
        print("Error for URL")
        return None

def getcomment(i, product_number):

    url1 = 'http://deal.11st.co.kr/product/SellerProductDetail.tmall?method=getProductReviewList&prdNo='
    product_number = str(product_number)
    url3 = '&page='
    url4 = i
    url5 = '&pageTypCd=first&reviewDispYn=Y&isPreview=false&reviewOptDispYn=Y&optSearchBtnAndGraphLayer=Y&reviewBottomBtn=Y&openDetailContents=Y&pageSize=100&isIgnoreAuth=false&lctgrNo=1001397&leafCtgrNo=0&groupProductNo=0&groupFirstViewPrdNo=0&selNo=41580890#this'

    url = url1 + product_number + url3 + url4 + url5
    #print(url)
    return url

def dataHandling(soup,product_number):
    df_feed_code = []
    df_review = []
    df_date = []
    df_star = []
    df_product = []

    #리뷰 모으기
    reviews = soup.select(
    'p.bbs_summary > span.summ_conts > a'
    )

    for review in reviews :
        review_ = review.text
        review_clean = review_.replace('\n', '')
        review_clean = review_clean.replace('\r', '')
        review_clean = review_clean.replace('\t', '')
        df_review.append(review_clean)
        #print(review_clean)

    #날짜 모으기
    dates = soup.select(
        'span.date'
    )

    for date in dates :
        date = date.text
        df_date.append(date)
        #print(date)

    #평점 모으기
    stars = soup.select(
     'div.bbs_top > div.top_l > div > p > span'
    )
    for star in stars :
        star = star.text
        star_clean = int(re.findall('\d', str(star))[1])
        df_star.append(star_clean)
        #print(star_clean)

    #구매한 상품 모으기
    products = soup.select(
        'div.bbs_cont_wrap > div.bbs_cont > p.option_txt'
    )
    for product in products :
        product = product.text
        df_product.append(product)
        #print(product)

    #feed code 부여하기
    codes = soup.select('p.bbs_summary')

    for code in codes :
        code_imsi = code.get('data-contno')
        #print(code_imsi)
        code_sum = '11st_' + '%s_'%(product_number) + str(code_imsi)
        df_feed_code.append(code_sum)

    print(len(df_review),len(df_star),len(df_date),len(df_product))

    if len(df_review) ==len(df_star) == len(df_date) == len(df_product) :
        pass
    else :
        return None

    # 구매평, 날짜, 평점, 상품을 합하여 하나의 데이터 프레임으로 생성
    df1 = pd.DataFrame({'feed_code':df_feed_code,'content':df_review, 'date':df_date, 'star':df_star, 'product_select':df_product})
    df1 = df1[['feed_code','content', 'date', 'star', 'product_select']]
    return df1


def main():
    for j in count():
        data_result = pd.DataFrame(columns=('feed_code', 'content', 'date', 'star', 'product_select'))
        url_imsi = []
        url_imsi = (str(input('{0}번째 url을 입력하세요 : '.format(j + 1))))
        p = re.compile('prdNo=\d+')
        product_number = str(p.search(url_imsi).group())
        product_number = product_number.replace('prdNo=', '')
        print(product_number)

        # 800페이지 까지 크롤링 하겠다는 의미
        for i in range(1,800):
            i = str(i)
            url = getcomment(i, product_number)
            soup = get_request_url(url)
            df1 = dataHandling(soup, product_number)
            data_result = pd.concat([data_result, df1], axis=0)

        print(data_result)
        data_result.to_csv('data_11st_%s.csv'%(product_number), mode='w', encoding='utf-8', index=False)
        print('저장 완료')

if __name__ == "__main__":
    main()

# db연결해서 저장하는 부분 수정하기

