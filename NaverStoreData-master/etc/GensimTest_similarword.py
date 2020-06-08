import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import word2vec

model = word2vec.Word2Vec.load("c:/pythondata/toji.model")
print(model.most_similar(positive=["땅"]))
