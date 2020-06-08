# 명사, 형용사, 조사 추출 (테이블로 데이터 저장)
# -*- coding:utf8 -*-

from konlpy.tag import Twitter
import pandas as pd

twitter = Twitter()

df = pd.read_csv("C:/naverstore/living_data1.csv")
data = df[df['content'].notnull()]
lines = data['content']

a = []
b = []

for line in lines:
    # print("@주어진 문장")
    # print("->" + line)
    for sentence in line.split(" "):
        buf = []
        # PROCESS one sentence
        for word in twitter.pos(sentence, stem=True, norm=True):
            if word[1] == 'Josa':
                buf.append(word)
                a.append(word[0])
                b.append(word[1])
                # print(word[0], word[1])
            if word[1] == 'Noun':
                buf.append(word)
                a.append(word[0])
                b.append(word[1])
                # print(word[0], word[1])
            if word[1] == 'Adjective':
                buf.append(word)
                a.append(word[0])
                b.append(word[1])
                # print(word[0], word[1])
        # print("buffer : " + str(buf))

data = pd.DataFrame({'단어':a, '품사':b})
# print(data)

data.to_csv('data_pos.csv', mode = 'w', index = True, encoding='utf-8', index_label= False)

