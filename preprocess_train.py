import gensim, logging
from gensim.models import Word2Vec, word2vec
import string
#import unicodedata
import collections
import tarfile
import unidecode
import os.path
import nltk

import spacy
#nlp = spacy.load('fr')
from spacy.lang.fr.stop_words import STOP_WORDS
#import fr_core_news_sm #spacy




def decode_string(sb):
    #return ''.join(filter(lambda x: x in string.printable, bytes(sb, "utf-8").decode("unicode_escape")))
    return unidecode.unidecode(sb)


def get_stopwords(STOP_WORDS):
    punctuations = string.punctuation
    stopchars = punctuations 
    stopwords_ = {'et','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z'}
    stopwords = STOP_WORDS.union(stopwords_)        
    return stopwords, stopchars



def text_process(mess, stopwords, stopchars, nlp, dedoubl=True):
    """
    Takes in a string of text, then performs the following:
    - lowerize string
    - Remove all punctuation
    - Remove all stopwords
    - Returns a list of the cleaned text
    """
    #lemmatize message
    #doc = nlp(mess)
    #mess = ' '.join([( word.lemma_) for word in doc])
    
    #remove accents
    mess = decode_string(mess)

    #remove punctuations + concat chars
    nopunc = ''.join([char if char not in stopchars else ' ' for char in mess]).replace('’',' ').replace('œ','oe')

    #remove stop words + remove digits + lowerize
    tokens = ' '.join([word.lower() for word in nopunc.split() if (word.lower() not in stopwords and not word.lower().replace(' ','').isdigit())]) 
    
    if dedoubl:
        tokens = [word for word in tokens.split()]
        return ' '.join(tokens)
    else:
        return tokens
    
    
    
def words_count(list_):
    wordcount = {}
    stopwords = get_stopwords(STOP_WORDS)
    for line in list_:
        for word in line.split():
            if word not in stopwords:
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1
                
    return collections.Counter(wordcount)


if __name__ == '__main__':
    print('start')
    print('TODO python -m spacy download fr')
    

    if not os.path.isfile('doc.txt'): 
        tar = tarfile.open("doc.txt.tar.bz2")
        tar.extractall()
        tar.close()
        print('untared file')
        
    with open('doc.txt', 'r') as f:
        docs = f.readlines()
        
    print('\ndocs avant preprocess ')
    print(len(docs))
    
    nltk.download('punkt')
    print('string.punctuation: ')
    print(string.punctuation)

    stopwords, stopchars = get_stopwords(STOP_WORDS)
    #nlp = fr_core_news_sm.load()
    nlp = spacy.load('fr')
    documents = [text_process(item, stopwords, stopchars, nlp) for item in docs]
    print('\ndocs preprocessed\n'.format(documents[0]))
          
    #word_counter is a collections.Counter()
    word_counter = words_count(documents)
    print('\nword counter')
    print(word_counter.most_common(len(word_counter) // 100))
    
    print(documents[:2])
    print('training model')
    model = gensim.models.Word2Vec (documents, size=160, window=10, min_count=2, workers=10)
    model.train(documents,total_examples=len(documents),epochs=10)
    model.save('w2v.model')
    print('model trained')
