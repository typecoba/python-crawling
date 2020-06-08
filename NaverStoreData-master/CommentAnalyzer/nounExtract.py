# 명사 빈도수 체크 (작성중)

import pandas as pd
from konlpy.tag import Twitter
from collections import Counter
import sqlite3

#Twitter 형태소 분석기로 명사를 추출하고 Dataframe 생성
def nounExtract(data):
    nlp = Twitter()

    a = ['만족', '보통', '불만']

    for i in a:
        _data = data[data['prefer'] == str(i)]
        text = ''
        try:
            for j in _data['content']:
                text += '' + str(j)
            print('%s text 추출 성공' % i)
            nouns = nlp.nouns(text)
            count = Counter(nouns)
            a = []
            b = []
            for k in count.items():
                a.append(k[0])
                b.append(k[1])
            if i == '만족':
                df1 = pd.DataFrame({'만족도': '만족', '단어': a, '빈도수': b})
                df1 = df1[['만족도', '단어', '빈도수']]
                df1 = df1.sort_values(by='빈도수', ascending=False)
            elif i == '보통':
                df2 = pd.DataFrame({'만족도': '보통', '단어': a, '빈도수': b})
                df2 = df2[['만족도', '단어', '빈도수']]
                df2 = df2.sort_values(by='빈도수', ascending=False)
            else:
                df3 = pd.DataFrame({'만족도': '불만', '단어': a, '빈도수': b})
                df3 = df3[['만족도', '단어', '빈도수']]
                df3 = df3.sort_values(by='빈도수', ascending=False)
            print('%s 명사 추출 성공' % i)
        except Exception as e:
            print(e)

    _df12 = pd.merge(df1[['단어', '빈도수']], df2[['단어', '빈도수']], on='단어', how='outer')
    _df123 = pd.merge(_df12, df3[['단어', '빈도수']], on='단어', how='outer')
    _df123 = _df123.fillna(0)
    _df123['빈도수합계'] = _df123[['빈도수_x', '빈도수_y', '빈도수']].apply(sum, axis=1).astype(int)
    dfTotal = _df123[['단어', '빈도수합계']]

    data = pd.concat([df1, df2, df3])
    data = data.reset_index()[['만족도', '단어', '빈도수']]

    return (data, dfTotal)

# 전체 단어빈도수와 만족도별 단어빈도수 DataFrame을 DB table에 저장하는 함수
def createDB(data1, data2, s_name, p_number):
    try:
        conn = sqlite3.connect("naverComment.db")
        cur = conn.cursor()

        cur.execute('drop table if exists nouns_total_{0}_{1}'.format(s_name, p_number))
        data1.to_sql('nouns_total_{0}_{1}'.format(s_name, p_number), conn)

        cur.execute('drop table if exists nouns_prefer_{0}_{1}'.format(s_name, p_number))
        data2.to_sql('nouns_prefer_{0}_{1}'.format(s_name, p_number), conn)
        print("Create DB Success")

        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        print("Error for createDB")
        return None

def main(s_name, p_number):
    data = pd.read_csv("csv_data/CommentData_{0}_{1}.csv".format(s_name, p_number), encoding="utf-8")

    df = nounExtract(data)
    dfPrefer = df[0]
    dfTotal = df[1]

    createDB(dfTotal, dfPrefer, s_name, p_number)

    dfTotal.to_csv('csv_data/nouns_total_{0}_{1}.csv'.format(s_name, p_number), mode='w', index=True, encoding='utf-8', index_label=False)
    dfPrefer.to_csv('csv_data/nouns_prefer_{0}_{1}.csv'.format(s_name, p_number), mode='w', index=True, encoding='utf-8', index_label=False)

if __name__ == "__main__":
    main()
