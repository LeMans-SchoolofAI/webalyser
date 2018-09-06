from gensim.models import Word2Vec, word2vec

docs = ['quartier']

w2v_model = Word2Vec.load('w2v.model')
print(w2v_model.wv.vocab)

raise

#myList = (model.wv.most_similar (positive=docs,topn=10))
#print([str(p[0]) for p in myList ])
print(w2v_model.wv.most_similar (positive=docs,topn=1))
