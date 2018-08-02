import gensim
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim.models import KeyedVectors



num_features = 300
min_word_count = 10

num_workers = 2
context = 4

downsampling = 0

# model = gensim.models.Word2Vec(w2v_data, workers=num_workers, size=num_features, min_count=min_word_count
#                               , window=context,sample = downsampling)

model =  gensim.models.Word2Vec.load(datapath("/home/alice/yeongmin/dataset/ko.bin"))

#
print(model.vector_size)
vector = model.wv.get_vector('갤럭시')
print(vector)
print(model.wv.most_similar('갤럭시'))
print( len(model.wv.vocab))

print(model.wv.most_similar(positive=[vector], topn=1)) ## vector를 글자로 바꾸기!