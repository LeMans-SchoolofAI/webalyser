import gensim, logging
from gensim.models import Word2Vec, word2vec
import os.path
import tarfile

def read_input(input_file):
    if not os.path.isfile(input_file): 
        tar = tarfile.open(input_file+".tar.bz2")
        tar.extractall()
        tar.close()
        print('untared file')
        
    with open(input_file, 'r') as f:
        docs = f.readlines()
    return docs

if __name__ == '__main__':
    print('start')  
    
    documents = read_input('preprocessed_docs.txt')
    print('\n'+str(len(documents))+' docs avant training')
    
    print('training model')
    model = gensim.models.Word2Vec (documents, size=160, window=10, min_count=2, workers=10)
    model.train(documents,total_examples=len(documents),epochs=10)
    model.save('w2v.model')
    
    myList = (model.wv.most_similar (positive='regularisation',topn=10))
    print([str(p[0]) for p in myList ])
    