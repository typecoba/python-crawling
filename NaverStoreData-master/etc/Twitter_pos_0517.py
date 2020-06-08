
#단어의 품사별로 나눈 예시(github)

# -*- coding:utf8 -*-

import sys
import json
import operator

from konlpy.tag import Kkma
from konlpy.utils import pprint
from konlpy.tag import Twitter

twitter = Twitter()

lines = [
    '프리미엄 댓 글, 적극 추천, 쿠션 감도 좋고 이뻐요',
 '그런데 제가 발 볼이 있어 크다는 소리에도 정 사이즈 시켰는데 헐렁거리네요 샌들은 발뒤꿈치가 살짝 나와야 하는데 ,2018-05-16 '
 '11:58 :521, 프리미엄 댓 글, 적극 추천, 베이지 240 샀다가 엄마 껄 로 235 핑크 추가 구매했습니다',
 '편하고 좋아요',
 '디자인도 이쁘고 무난하니 여름 바지나 치마 아무 거에 나 다 잘 어울릴 것 같아요,',
 '프리미엄 댓 글, 적극 추천, 걸어 본건 아니지만 신발이 막 들어가고 쑥쑥 벗겨져요',
 '왜 지퍼가 있는 진 모르겠어요'
]

"pos---------------------------"
"""
	Hueristic Method
	=> 명사, 조사, 형용사 추출
	=> concat Nouns
	=> REGEX ; (명사+조사)+형용사
"""
for line in lines:
    print("@주어진 문장")
    print("->" + line)
    for sentence in line.split("."):
        buf = []
        # PROCESS one sentence
        for word in twitter.pos(sentence, stem=True):
            if word[1] == 'Josa':
                buf.append(word)
                print(word[0], word[1])
            if word[1] == 'Noun':
                buf.append(word)
                print(word[0], word[1])
            if word[1] == 'Adjective':
                buf.append(word)
                print(word[0], word[1])
        print("buffer : " + str(buf))

