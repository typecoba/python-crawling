# 명사 빈도수 체크 (작성중)

# -*- coding: utf-8 -*-

import pandas as pd
from collections import Counter
from konlpy.tag import Twitter
from konlpy.utils import pprint
from collections import Counter

data = pd.read_csv("C:/naverstore/living_data1.csv")

nlp = Twitter()

text = ''
data01 = data[data['prefer'] == '만족' ]

for item in data01['content'] :
    try :
        text += item
    except Exception as e:
        print(e)

nouns = nlp.nouns(text)
count = Counter(nouns)
print('만족한 사람들 반응')
print(count)

wordinfo = dict()
for tags, counts in count.most_common(200):
    if(len(str(tags))>1) :
        wordinfo[tags] = counts

data_nouns = pd.DataFrame.from_dict(wordinfo, orient='index')


text = ''
data02 = data[data['prefer'] == '보통' ]
for item in data02['content'] :
    try :
        text += item
    except Exception as e:
        print(e)

nouns = nlp.nouns(text)
count = Counter(nouns)
print('보통인 사람들 반응')
print(count)


text = ''
data03 = data[data['prefer'] == '불만' ]
for item in data03['content'] :
    try :
        text += item
    except Exception as e:
        print(e)

nouns = nlp.nouns(text)
count = Counter(nouns)
print('불만인 사람들 반응')
print(count)

data_nouns.to_csv('data_nouns2.csv', mode = 'w', index = True, encoding='utf-8', index_label= False)

