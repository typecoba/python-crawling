from wordcloud import WordCloud
from PIL import Image
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
# matplotlib 폰트 한글 지원
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
from matplotlib import style
style.use('ggplot')

#데이터 전처리하는 함수
def dataHandling(dfTotal, df):
    # df와 dfTotal의 컬럼명을 같도록 한다.
    dfTotal.rename(columns={'빈도수합계': '빈도수'}, inplace=True)

    text = open('korean_stopword_dic.txt', encoding='utf-8').read()

    # 한글 불용어 사전으로 불용어 제거
    p = re.compile('[가-힣]+')
    text = p.findall(text)

    for i in text:
        dfTotal = dfTotal[dfTotal['단어'] != str(i)]
        df = df[df['단어'] != str(i)]

    #불용어 제거 후 인덱스 재정의
    dfTotal = dfTotal.reset_index()[['단어', '빈도수']]
    df = df.reset_index()[['만족도', '단어', '빈도수']]
    df1 = df[df['만족도'] == '만족']
    df1 = df1[['단어', '빈도수']]
    df2 = df[df['만족도'] == '보통']
    df2 = df2.reset_index()[['단어', '빈도수']]
    df3 = df[df['만족도'] == '불만']
    df3 = df3.reset_index()[['단어', '빈도수']]

    return (dfTotal, df1, df2, df3)

#wordcloud와 barplot을 생성하여 이미지 저장
def createChart(df_list, s_name, p_number):
    count = 1

    for i in df_list:
        nouns = list(i['단어'].loc[0:9])
        nouns.reverse()
        freq = list(i['빈도수'].loc[0:9])
        freq.reverse()

        plt.figure(figsize=(5.5, 4))
        rects = plt.barh(np.arange(10), freq, align='center', height=0.6, color = 'skyblue')
        plt.yticks(np.arange(10), nouns)

        for k, rect in enumerate(rects):
            plt.text(0.99 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0,
                     str(freq[k]), ha='right', va='center')
        plt.xlabel('빈도수')
        plt.title('TOP 10 단어 빈도수', size=20)

        if count == 1:
            fig = plt.gcf()
            fig.savefig('image_data/total_bar_{0}_{1}.jpg'.format(s_name, p_number))
        elif count == 2:
            fig = plt.gcf()
            fig.savefig('image_data/good_bar_{0}_{1}.jpg'.format(s_name, p_number))
        elif count == 3:
            fig = plt.gcf()
            fig.savefig('image_data/moderate_bar_{0}_{1}.jpg'.format(s_name, p_number))
        else:
            fig = plt.gcf()
            fig.savefig('image_data/bad_bar_{0}_{1}.jpg'.format(s_name, p_number))
        #마스킹 이미지 수치화
        mask = np.array(Image.open('Mask.png'))
        #data를 dict형으로 변환
        a = {}
        for j in range(i.shape[0]):
            a[i.loc[j][0]] = i.loc[j][1]

        #wordcloud 생성자 지정 및 객체생성
        wordcloud = WordCloud(font_path='DXPOP-KSCpc-EUC-H.ttf',
                              relative_scaling=0.3, mask=mask,
                              background_color='white',
                              min_font_size=1, max_font_size=80
                              ).generate_from_frequencies(a)

        plt.figure(figsize=(5.5, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        if count == 1:
            fig = plt.gcf()
            fig.savefig('image_data/total_wc_{0}_{1}.jpg'.format(s_name, p_number))
        elif count == 2:
            fig = plt.gcf()
            fig.savefig('image_data/good_wc_{0}_{1}.jpg'.format(s_name, p_number))
        elif count == 3:
            fig = plt.gcf()
            fig.savefig('image_data/moderate_wc_{0}_{1}.jpg'.format(s_name, p_number))
        else:
            fig = plt.gcf()
            fig.savefig('image_data/bad_wc_{0}_{1}.jpg'.format(s_name, p_number))

        count = count + 1

def main(s_name, p_number):
    dfTotal = pd.read_csv('csv_data/nouns_total_{0}_{1}.csv'.format(s_name, p_number), encoding="utf-8")
    df = pd.read_csv('csv_data/nouns_prefer_{0}_{1}.csv'.format(s_name, p_number), encoding="utf-8")

    df_list = dataHandling(dfTotal, df)

    createChart(df_list, s_name, p_number)

if __name__ == "__main__":
    main()
