install.packages("extrafont")

library(KoNLP)
library(dplyr)
library(stringr)
library(wordcloud)
library(RColorBrewer)
library(extrafont)
useNIADic()

# 카테고리 만족도별 워드클라우드
setwd("C:\\workspace\\MyDjango\\NaverShopping")
getwd()
baby_nouns <- read.csv("baby_nouns.csv", header = T, stringsAsFactors = F, fileEncoding = "UTF-8")

baby_good <- baby_nouns[baby_nouns$만족도 == "만족", ]
baby_good <- baby_good[baby_good$단어 != "배송" & baby_good$단어 != "너무" & baby_good$단어 != "가격" & baby_good$단어 != "구매" & baby_good$단어 != "그냥" & baby_good$단어 != "좀" & baby_good$단어 != "아직" & baby_good$단어 != "별로" & baby_good$단어 != "보통" & baby_good$단어 != "생각" & baby_good$단어 != "제품" & baby_good$단어 != "상품" & baby_good$단어 != "때" & baby_good$단어 != "더" & baby_good$단어 != "것" & baby_good$단어 != "요" & baby_good$단어 != "거", ]

baby_normal <- baby_nouns[baby_nouns$만족도 == "보통", ]
baby_normal <- baby_normal[baby_normal$단어 != "배송" & baby_normal$단어 != "너무" & baby_normal$단어 != "가격" & baby_normal$단어 != "구매" & baby_normal$단어 != "그냥" & baby_normal$단어 != "좀" & baby_normal$단어 != "아직" & baby_normal$단어 != "별로" & baby_normal$단어 != "보통" & baby_normal$단어 != "생각" & baby_normal$단어 != "제품" & baby_normal$단어 != "상품" & baby_normal$단어 != "때" & baby_normal$단어 != "더" & baby_normal$단어 != "것" & baby_normal$단어 != "요" & baby_normal$단어 != "거", ]

baby_bad <- baby_nouns[baby_nouns$만족도 == "불만", ]
baby_bad <- baby_bad[baby_bad$단어 != "배송" & baby_bad$단어 != "너무" & baby_bad$단어 != "가격" & baby_bad$단어 != "구매" & baby_bad$단어 != "그냥" & baby_bad$단어 != "좀" & baby_bad$단어 != "아직" & baby_bad$단어 != "별로" & baby_bad$단어 != "보통" & baby_bad$단어 != "생각" & baby_bad$단어 != "제품" & baby_bad$단어 != "상품" & baby_bad$단어 != "때" & baby_bad$단어 != "더" & baby_bad$단어 != "것" & baby_bad$단어 != "요" & baby_bad$단어 != "거", ]

pal <- brewer.pal(9,"Set3")  
set.seed(1234)
font_import() # y 입력
loadfonts(device="win")
windowsFonts(malgun=windowsFont("맑은 고딕"))
windowsFonts(headline=windowsFont("HY헤드라인M"))
windowsFonts(baedal=windowsFont("배달의민족 연성"))

wordcloud(words = baby_good$단어,
          freq = baby_good$빈도수,
          max.word = 400,
          random.order = F,
          random.color = T,
          rot.per = .1,
          scale = c(4, 0.5),
          colors = pal,
          family="malgun")



