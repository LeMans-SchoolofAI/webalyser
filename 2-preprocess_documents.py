
# coding: utf-8

# In[1]:


import string
import collections
import tarfile
import unidecode
import os.path
import nltk


# In[2]:


#import spacy
#from spacy.lang.fr.stop_words import STOP_WORDS
#nlp = spacy.load('fr')

#loading STOP_WORDS from local file instead of Spacy lib
with open('stop_words.txt', 'r') as f:
    words = f.readlines()
STOP_WORDS = set([word.strip() for word in words])


# In[3]:


def decode_string(sb):
    return unidecode.unidecode(sb)


# In[4]:


def get_stopwords(STOP_WORDS):
    punctuations = string.punctuation
    stopchars = punctuations 
    stopwords_ = {'et','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z'}
    stopwords = STOP_WORDS.union(stopwords_)        
    return stopwords, stopchars


# In[5]:


def text_process(mess, stopwords, stopchars, dedoubl=True):
    #lemmatize message
    #doc = nlp(mess)
    #mess = ' '.join([( word.lemma_) for word in doc])
    
    #remove accents
    mess = decode_string(mess)

    #remove punctuations + concat chars
    nopunc = ''.join([char if char not in stopchars else ' ' for char in mess]).replace('’',' ').replace('œ','oe')

    #remove stop words + remove digits + lowerize
    tokens = ' '.join([word.lower() for word in nopunc.split() if (word.lower() not in stopwords and not word.lower().replace(' ','').isdigit())]) 
    
    tokens = [word for word in tokens.split()]
    
    if dedoubl:
<<<<<<< HEAD:2-preprocess_documents.py
        return list(set(tokens))
=======
        tokens = [word for word in tokens.split()]
        return ' '.join(tokens)
>>>>>>> c24dbe895aac18127b9698d74d2c628d7472ff07:preprocess_train.py
    else:
        return tokens


# In[6]:


def words_count(list_,stopwords):
    wordcount = {}
    for line in list_:
        for word in line:
            if word not in stopwords:
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1
                
    return collections.Counter(wordcount)


# In[7]:


def read_input(input_file):
    if not os.path.isfile(input_file): 
        tar = tarfile.open(input_file+".tar.bz2")
        tar.extractall()
        tar.close()
        print('untared file')
        
    with open(input_file, 'r') as f:
        docs = f.readlines()
        
<<<<<<< HEAD:2-preprocess_documents.py
    return docs


# In[8]:


def write_output(output_file):
    with open(output_file, "w") as f:
        for s in docs:
            f.write(str(s) +"\n")

    tar = tarfile.open(output_file+".tar.bz2", "w:bz2")
    tar.add(output_file)
    tar.close()
    os.remove(output_file)


# In[9]:


if __name__ == '__main__':
    print('start')  
    
    docs = read_input('doc.txt')
    print('\n'+str(len(docs))+' docs avant preprocessing')
    print(docs[0])
    
    nltk.download('punkt')
    print('string.punctuation : '+string.punctuation)

    stopwords, stopchars = get_stopwords(STOP_WORDS)
    documents = [text_process(item, stopwords, stopchars) for item in docs]
    print('\ndocs preprocessed')
    print(documents[0])
    
    #word_counter is a collections.Counter()
    word_counter = words_count(documents,stopwords)
    print('\nword counter')
    print(word_counter.most_common(len(word_counter) // 100))
    
    write_output('preprocessed_docs.txt')

=======
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
>>>>>>> c24dbe895aac18127b9698d74d2c628d7472ff07:preprocess_train.py
