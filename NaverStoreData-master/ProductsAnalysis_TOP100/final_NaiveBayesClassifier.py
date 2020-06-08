from nltk.classify import NaiveBayesClassifier
import pandas as pd
import re

# KOSAC사전에서 polarity.csv 파일을 불러온다. ngram.과 max.value 행만 사용하도록 df 내용 수정.
df_dic = pd.read_csv("C:/naverstore/lexicon/mypolarity.csv", encoding='utf-8')
df = df_dic[df_dic['max.value'].notnull()]
df = df[['ngram','max.value']]

# 한글과 영문이 섞여있는 ngram에서, 가장 앞에 있는 한글단어만 추출하는 정규 표현식
p = r'^[가-힣]+'

# KOSAC으로 부터 긍정(POS), 부정(NEG), 중립(NEU)의 사전을 생성한다
pos_dic = []
neg_dic = []
neu_dic = []

for i, row in df.iterrows():
    if row['max.value'] ==  'POS':
        pos_dic.extend(re.findall(p, row['ngram']))
    elif row['max.value'] ==  'NEG':
        neg_dic.extend(re.findall(p, row['ngram']))
    elif row['max.value'] ==  'NEUT':
        neu_dic.extend(re.findall(p, row['ngram']))

# 중복 단어를 제거하기 위해서 set로 만들었다가 list로 변환시킨다
positive_vocab = list(set(pos_dic)) #총 1830개 단어
negative_vocab = list(set(neg_dic)) #총 1623개 단어
neutral_vocab = list(set(neu_dic)) #총 340개 단어

def word_feats(words):
    return dict((word, True) for word in words)

# 사전의 긍정, 부정, 중립단어를 navie bayes에 학습시킬 준비를 한다
positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]

# 트레인 데이터셋 생성 완료! naive bayes에 학습 시킨다
train_set = negative_features + positive_features + neutral_features
classifier = NaiveBayesClassifier.train(train_set)

# 예측하기 위해 데이터셋 준비(_data.csv 앞에 글자만 작성. beauty를 예시로 써둠)
name = "beauty"

df = pd.read_csv("C:/naverstore/final/%s_data.csv"%(name))
data = df[df['content'].notnull()]
print('총 문장수는 '+ str(len(data)) + '개 입니다')

neg = 0; pos = 0 ;neu = 0;
pos_word = ['POS'] ; neg_word = ['NEG'] ;neu_word = ['NEU'];

# for문으로 예측하고 싶은 문장을 돌려서 한 문장씩 예측 시킨다
for sentence in data['content']:
    sentence = sentence.lower()
    words = sentence.split(',')

    for word in words:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
            neg_word.append(word)
        elif classResult == 'pos':
            pos = pos + 1
            pos_word.append(word)
        elif classResult == 'neu' :
            neu = neu +1
            neu_word.append(word)

# 결과 출력시키기
print('긍정의 문장 수는 ' + str(pos) +'개 입니다')
print('부정의 문장 수는 ' + str(neg) +'개 입니다')
print('중립의 문장 수는 ' + str(neu) +'개 입니다')

print('긍정인 반응은 ' + str(float(pos)*100 / len(data['content'])) + '% 입니다')
print('부정인 반응은 ' + str(float(neg)*100 /  len(data['content'])) + '% 입니다')
print('중립인 반응은 ' + str(float(neu)*100 /  len(data['content'])) + '% 입니다')

# 긍정, 부정, 중립의 문장을 가장 많이 나온 순으로 나열하여 csv 파일로 저장
three_type = [pos_word, neg_word, neu_word]

for one_type in three_type:
    w_count = {}
    for idx,  one_sentence in enumerate(one_type):
        if idx == 0:
            continue
        try: w_count[one_sentence] +=1
        except: w_count[one_sentence] = 1
    pd_data = pd.DataFrame(list(w_count.items()))
    pd_data.columns = ['sentence', 'count']
    pd_data = pd_data.sort_values('count', ascending=False)
    pd_data.to_csv('data_%s_%s.csv'%(name, one_type[0]), mode = 'w', index = False, encoding='utf-8', index_label= False)

print('csv 파일로(3개) 저장 완료')

