from konlpy.tag import Twitter
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import word2vec
import codecs
from bs4 import BeautifulSoup

fp = codecs.open("C:/pythondata/BEXX0003.txt", "r", encoding="utf-8")
soup = BeautifulSoup(fp, "html.parser")
body = soup.select_one("body > text")
text = body.getText()

twitter = Twitter()
results = []
lines = text.split('\r\n')

for line in lines :
    malist = twitter.pos(line, norm=True, stem=True)
    r = []
    for word in malist:
        if not word[1] in ["Josa", "Eomi", "Punctuation"]:
            r.append(word[0])
    rl = (" ".join(r)).strip()
    results.append(rl)

print(results)

wakati_file = 'c:/pythondata/tojifile.txt'

with open(wakati_file, 'w', encoding='utf-8') as fp:
    fp.write("\n".join(results))

data = word2vec.LineSentence(wakati_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
model.save("c:/pythondata/toji.model")
print("ok")
