import gensim, logging
from gensim.models import Word2Vec, word2vec
import os.path
import tarfile
import pickle

def read_input(input_file):
    if not os.path.isfile(input_file): 
        tar = tarfile.open(input_file+".tar.bz2")
        tar.extractall()
        tar.close()
        print('untared file')
        
    with open(input_file, 'rb') as handle:
        return pickle.load(handle)


if __name__ == '__main__':
    print('start')  
    documents_list = read_input('preprocessed_docs.txt.pickle')
    print('\n'+str(len(documents_list))+' docs avant training')
    
    print('training model')
    model = gensim.models.Word2Vec (len(documents_list), size=160, window=10, min_count=2, workers=10)
    model.train(documents,total_examples=len(len(documents_list)),epochs=10)
    model.save('w2v.model')
    
    myList = (model.wv.most_similar (positive='regularisation',topn=10))
    print([str(p[0]) for p in myList ])
    