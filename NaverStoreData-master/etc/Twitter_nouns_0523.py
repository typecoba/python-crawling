# 명사 빈도수 체크 (테이블로 데이터 저장)

# -*- coding: utf-8 -*-

import pandas as pd

from konlpy.tag import Twitter
from collections import Counter

data = pd.read_csv("C:/untitled/living_data1.csv")

nlp = Twitter()

a = ['만족', '보통', '불만']

for i in a:
    _data = data[data['prefer'] == str(i)]
    text = ''
    for j in _data['content']:
        try:
            text += '' + str(j)
        except Exception as e:
            print(e)
    nouns = nlp.nouns(text)
    count = Counter(nouns)
    a = []
    b = []
    for k in count.items():
        a.append(k[0])
        b.append(k[1])
    if i == '만족':
        df1 = pd.DataFrame({'만족도':'만족','단어':a, '빈도수':b})
        df1 = df1[['만족도','단어','빈도수']]
        df1 = df1.sort_values(by = '빈도수', ascending=False)
    elif i == '보통':
        df2 = pd.DataFrame({'만족도':'보통','단어':a, '빈도수':b})
        df2 = df2[['만족도','단어','빈도수']]
        df2 = df2.sort_values(by = '빈도수', ascending=False)
    else:
        df3 = pd.DataFrame({'만족도':'불만','단어':a, '빈도수':b})
        df3 = df3[['만족도','단어','빈도수']]
        df3 = df3.sort_values(by = '빈도수', ascending=False)

data = pd.concat([df1,df2,df3])
data = data.reset_index()[['만족도','단어','빈도수']]

data.to_csv('data_nouns2.csv', mode = 'w', index = True, encoding='utf-8', index_label= False)
