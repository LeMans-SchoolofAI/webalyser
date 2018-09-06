from gensim.models import Word2Vec, word2vec
import unidecode
import string

import nltk
nltk.download('punkt')

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import fr_core_news_sm #spacy


def decode_string(sb):
    return unidecode.unidecode(sb)


def get_stopwords(STOP_WORDS):
    punctuations = string.punctuation
    stopchars = punctuations 
    stopwords_ = {'et','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z'}
    stopwords = STOP_WORDS.union(stopwords_)        
    return stopwords, stopchars


def text_process(mess, stopwords, stopchars, nlp, dedoubl=True):
    #lemmatize message
    doc = nlp(mess)
    mess = ' '.join([( word.lemma_) for word in doc])
    
    #remove accents
    mess = decode_string(mess)

    #remove punctuations + concat chars
    nopunc = ''.join([char if char not in stopchars else ' ' for char in mess]).replace('’',' ').replace('œ','oe')

    #remove stop words + remove digits + lowerize
    tokens = ' '.join([word.lower() for word in nopunc.split() if (word.lower() not in stopwords and not word.lower().replace(' ','').isdigit())]) 
    
    if dedoubl:
        #tokens = stemming_dedoubl_txt(tokens)
        tokens = [word for word in tokens.split()]
        return ' '.join(tokens)
    else:
        #tokens = stemming_txt(toke        ns)
        return tokens


model = Word2Vec.load('w2v.model')
nltk.download('punkt')
#print(f'string.punctuation: {string.punctuation}')
stopwords, stopchars = get_stopwords(STOP_WORDS)
#nlp = fr_core_news_sm.load()
nlp = spacy.load('fr')

docs = ['cantine','école']
documents = [text_process(item, stopwords, stopchars, nlp) for item in docs]


myList = (model.wv.most_similar (positive=documents,topn=10))
print([str(p[0]) for p in myList ])