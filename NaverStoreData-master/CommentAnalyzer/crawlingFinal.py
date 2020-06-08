# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
import re
import sqlite3

def get_request_url(url_all):
    try:
        response = requests.get(url_all)
        if int(response.status_code) == 200:
            p = re.compile('premium.json')
            if bool(p.search(url_all)) == True:
                print("PremiumComment Url Request Success")
                return response.text
            else:
                print("GeneralComment Url Request Success")
                return response.text
    except Exception as e:
        print(e)
        print("Error for URL")
        return None


def getComment(s_name, p_number):
    url01 = 'http://smartstore.naver.com/'
    url03 = '/products/'
    url05 = '/purchasereviews/premium.json?sortType=PURCHASE_REVIEW_CREATED&evaluationGrade=&page.page=1&page.size=999'
    url_all1 = url01 + s_name + url03 + p_number + url05

    url01 = 'http://smartstore.naver.com/'
    url03 = '/products/'
    url05 = '/purchasereviews/general.json?satisfactionGrade=&page.page=1&page.size=999'
    url_all2 = url01 + s_name + url03 + p_number + url05

    plain_text1 = get_request_url(url_all1)
    plain_text2 = get_request_url(url_all2)

    mydatas = []
    for i in [plain_text1, plain_text2]:
        if (i == None):
            return None
        else:
            mydatas.append(json.loads(i))

    return mydatas


def dataHandling(mydatas):
    p_list_comment = []

    for comment in mydatas[0]['htReturnValue']['pagedResult']['content']:
        p_list_comment.append('프리미엄댓글')
        p_list_comment.append(comment['gradeText'])
        p_list_comment.append(comment['contentsSummary'])
        p_list_comment.append(comment['createdDate'])

    g_list_comment = []

    for comment in mydatas[1]['htReturnValue']['pagedResult']['content']:
        g_list_comment.append('일반댓글')
        g_list_comment.append(comment['gradeText'])
        g_list_comment.append(comment['title'])
        g_list_comment.append(comment['createdDate'])

    result = []
    _result = []

    for i in [p_list_comment, g_list_comment]:
        for item in i:
            _result.append(item)
            if len(_result) == 4:
                result.append(_result)
                _result = []

    data = pd.DataFrame(result, columns=('type', 'prefer', 'content', 'date'))

    j = 0
    p = re.compile('\w+')
    for item in data['content']:
        b = item.replace('\n', '')
        c = p.findall(b)
        k = ''
        for i in c:
            k += ' ' + str(i)
        data['content'][j] = k
        j += 1

    j = 0
    for i in data['prefer']:
        if str(i) == '적극추천' or str(i) == '추천':
            data['prefer'][j] = '만족'
            j += 1
        elif str(i) == '추천안함':
            data['prefer'][j] = '불만'
            j += 1

    return data

def createDB(data, s_name, p_number):
    try:
        conn = sqlite3.connect("naverComment.db")
        cur = conn.cursor()

        cur.execute('drop table if exists comment_{0}_{1}'.format(s_name, p_number))
        data.to_sql('comment_{0}_{1}'.format(s_name, p_number), conn)
        print("Create DB Success")

        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        print("Error for createDB")
        return None

def main(url):
    # url = str(input('url을 입력하세요 : '))

    _s_name = re.compile('\w+/products/')
    _p_number = re.compile('/products/\d+')

    s_name = str(_s_name.search(url).group()).replace('/products/','')
    p_number = str(_p_number.search(url).group()).replace('/products/','')
    print(s_name, p_number)

    mydatas = getComment(s_name, p_number)

    data = dataHandling(mydatas)

    data.to_csv('csv_data/CommentData_%s_%s.csv'%(s_name,p_number), mode = 'w', index = True,
                encoding='utf-8', index_label= False)

    createDB(data, s_name, p_number)

    return (s_name, p_number)

if __name__ == "__main__":
    main()
