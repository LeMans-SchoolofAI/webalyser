
# coding: utf-8

# In[ ]:


#main goal : don't load spacy lib in preprocess_train for easier reuse in meetup group
print('/!\ EXECUTE IF AND ONLY IF SPACY LIB IS INSTALLED ON YOUR SYSTEM')


# In[ ]:


from spacy.lang.fr.stop_words import STOP_WORDS


# In[ ]:


with open('stop.txt', 'r') as f:
    docs = f.readlines()


# In[ ]:


stops = set([doc.strip() for doc in docs])


# In[ ]:


stop_words = STOP_WORDS.union(stops)


# In[ ]:


with open("stop_words.txt", "w") as f:
    for s in stop_words:
        f.write(str(s) +"\n")

