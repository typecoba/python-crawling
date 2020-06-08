
from nltk.classify import NaiveBayesClassifier
import pandas as pd
from konlpy.tag import Twitter
import re

twitter = Twitter()

df_dic = pd.read_csv("C:/lexicon/polarity.csv", encoding='utf-8')

df = df_dic[df_dic['max.value'].notnull()]
df = df[['ngram','max.value']]

p = r'^[가-힣]+'

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

def word_feats(words):
    return dict((word, True) for word in words)

positive_vocab = list(set(pos_dic))
negative_vocab = list(set(neg_dic))
neutral_vocab = list(set(neu_dic))

positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]

train_set = negative_features + positive_features + neutral_features
classifier = NaiveBayesClassifier.train(train_set)

# Predict
neg = 0
pos = 0
neu = 0
df = pd.read_csv("C:/naverstore/final/comment_data.csv")
data = df[df['content'].notnull()]

for sentence in data['content']:
    sentence = sentence.lower()
    words = sentence.split(',')

    for word in words:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1
        if classResult == 'neu' :
            neu = neu +1

print(pos)
print(neg)
print(neu)

print('긍정인 반응은 ' + str(float(pos)*100 / (float(pos) + float(neg) + float(neu))) + '% 입니다')
print('부정인 반응은 ' + str(float(neg)*100 / (float(pos) + float(neg) + float(neu))) + '% 입니다')
print('중립인 반응은' + str(float(neu)*100 / (float(pos) + float(neg) + float(neu))) + '% 입니다')

