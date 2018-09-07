
# coding: utf-8

# In[ ]:


import pickle
import re
import unicodedata
import string
import tarfile
import os.path


# In[ ]:


def load_pickle(filename, **kwargs):
    for key, value in kwargs.items():
        filename_ = filename+'-'+key+'.pickle'

        if not os.path.isfile(filename_):
            tar = tarfile.open(filename_+'.tar.bz2')
            tar.extractall()
            tar.close()
        
        with open(filename_, 'rb') as handle:
            kwargs[key] = pickle.load(handle)
            
    return list(kwargs.values())
            


# In[ ]:


def save_pickle(filename, **kwargs):
    for key, value in kwargs.items():
        with open(filename+'-'+key+'.pickle', 'wb') as handle:
            pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:


def get_filename(root):
    chars_to_remove = ['.', '/', ':']
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    return re.sub(rx, '', root)


# In[ ]:


def decode_string(sb):
    return ''.join(filter(lambda x: x in string.printable, bytes(sb, "utf-8").decode("unicode_escape")))


# In[ ]:


def walk_on_pairs(dic,pos,nb):
    keys_list = list(dic.keys())[pos:pos+nb]
    for url in keys_list:
        print(url,'\n')
        print(dic[url],'\n')


# In[ ]:


def write_output(output_file):
    with open(output_file, "w") as f:
        for s in docs:
            f.write(str(s) +"\n")

    tar = tarfile.open(output_file+".tar.bz2", "w:bz2")
    tar.add(output_file)
    tar.close()
    os.remove(output_file)


# In[ ]:


root = 'http://www.lemans.fr' #website crawled
output_file = 'doc.txt'

links, passed_links = load_pickle(get_filename(root), links={}, passed_links={})
print(str(len(links))+' paires chargées')

docs = [value.replace('\n','').replace('\t','').replace('\r','') for key, value in links.items()]
write_output(output_file)
print(str(len(docs))+' paires exported')


# In[ ]:


walk_on_pairs(links,0,2)


# # Cleaning bad values

# ### DEAL with outdated browser message

# In[ ]:


outdated_browser_msg = 'outdated browser'


# In[ ]:


outdated_browser = [key for key, value in links.items() if outdated_browser_msg in value]
print(len(outdated_browser))


# In[ ]:


for page in outdated_browser:
    links[page] = False


# In[ ]:


save_pickle(get_filename(root), links=links, passed_links=passed_links)


# ### DEAL with pdf content pages

# In[ ]:


pdf_pages = [key for key, value in links.items() if (isinstance(value, str) and '%PDF-1' in value) or (key[-4:] == '.pdf') or (key[-8:] == 'type=125')]
print(len(pdf_pages))


# In[ ]:


for page in pdf_pages:
    passed_links[page]=False
    del links[page]


# In[ ]:


pdf_pages = [key for key, value in links.items() if (isinstance(value, str) and '%PDF-1' in value) or (key[-4:] == '.pdf') or (key[-8:] == 'type=125')]
print(len(pdf_pages))


# In[ ]:


save_pickle(get_filename(root), links=links, passed_links=passed_links)


# ### DEAL with .zip .pdf .jpg .png .jpeg pages

# In[ ]:


pages = [key for key, value in links.items() if (key[-4:] == '.zip') or (key[-4:] == '.pdf')  
                                             or (key[-4:] == '.jpg') or (key[-4:] == '.png') 
                                             or (key[-5:] == '.jpeg') or (key[-4:] == '.mp3')
                                             or (key[-4:] == '.dot') or (key[-4:] == '.doc')  
                                             or (key[-4:] == '.JPG')]
print(len(pages))


# In[ ]:


for page in pages:
    passed_links[page]=False
    del links[page]


# In[ ]:


pages = [key for key, value in links.items() if (key[-4:] == '.zip') or (key[-4:] == '.pdf')  
                                             or (key[-4:] == '.jpg') or (key[-4:] == '.png') 
                                             or (key[-5:] == '.jpeg') or (key[-4:] == '.mp3')
                                             or (key[-4:] == '.dot') or (key[-4:] == '.doc')  
                                             or (key[-4:] == '.JPG')]
print(len(pages))


# In[ ]:


save_pickle(get_filename(root), links=links, passed_links=passed_links)


# ### DEAL with 'le detail de l'actualite' pages

# In[ ]:


pages = [key for key, value in links.items() if 'details-de-lactualite' in key]
print(len(pages))


# In[ ]:


for page in pages:
    passed_links[page]=False
    del links[page]


# In[ ]:


pages = [key for key, value in links.items() if  'details-de-lactualite' in key]
print(len(pages))


# In[ ]:


save_pickle(get_filename(root), links=links, passed_links=passed_links)


# ### DEAL with undecodable pages

# In[ ]:


links, passed_links = load_pickle(get_filename(root))
links_ = links.copy()

for key, value in links.items():
    try:
        decode_string(value)
    except:
        print(key)
        passed_links[key]=False
        del links_[key]

        
save_pickle(get_filename(root), links=links_, passed_links=passed_links)

