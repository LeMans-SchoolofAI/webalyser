# webalyser
NLP website comprehension - gensim, spacy, word2vec

## datafiles
- httpwwwlemansfr-links.pickle : pickle file, dictionnary, content : key = URL, value = webpage text
- httpwwwlemansfr-passed_links.pickle : pickle file, dictionnary, content : key = dropped URL, value = False

## notebook jupyter
- 0-aggregate_stop_words.ipynb : prepare stop_words.txt file
- 1-sanitize_collected_datas.ipynb : clean pickle file
- 2-preprocess_documents.ipynb : prepare dataset for word2vec training
- (#notanotebook) training_word2vec.py : train word2vec model + try a prediction

## HTML collector
- unrefined script : collect.ipynb

