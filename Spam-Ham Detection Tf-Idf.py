#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install nltk -U


# In[2]:


import nltk
from nltk.corpus import stopwords
from pyhive import hive
import os
import pandas as pd
import re
import string
import numpy as np
import sys

nltk.download('stopwords')


# In[3]:


connection = hive.Connection(host="localhost",port=10000, auth="NOSASL",database="amazonreviews")
cursor = connection.cursor()
cursor.execute('set hive.execution.engine=mr')
cursor.execute('show databases')
cursor.fetchall()


# In[4]:


cursor.execute('select * from amazonreviews.amazonToys limit 10000')
amazonToys = cursor.fetchall()
toysDataset = pd.DataFrame(amazonToys, columns=['reviewerID','reviewerName','reviewText','summary','reviewDate','category','class']);


# In[5]:


spam_temp = toysDataset[toysDataset['class'] == 1] 
spam_dataset=pd.DataFrame(spam_temp)
ham_temp = toysDataset[toysDataset['class'] == 0]               #Considered non-spam as ham 
ham_dataset=pd.DataFrame(ham_temp) 


# In[6]:


ham_dataset


# In[7]:


spam_mapperout = [];
for ind in spam_dataset.index:
    single_line =spam_dataset['reviewText'][ind]
    doc_id = spam_dataset['reviewerID'][ind]
    single_line = single_line.lower().strip()
    single_line = re.sub(r"[^\w\s]", "", single_line)
    words = single_line.split()
    for word in words:
        isDigits = any(str.isdigit(c) for c in word)
        if len(word) > 3 and not isDigits and word not in stopwords.words('english'):
            print(word, doc_id, 1)
            spam_mapperout.append((word, doc_id, 1))
    
    
    
    # print(ham_dataset.loc[i, "reviewerID"], ham_dataset.loc[i, "reviewerName"],ham_dataset.loc[i, "reviewText"],ham_dataset.loc[i, "summary"],ham_dataset.loc[i, "reviewDate"],ham_dataset.loc[i, "category"],ham_dataset.loc[i, "class"])


# In[ ]:


currentCount = 0
currentKey = None
lastKey = None

for line in spam_mapperout:
    #print(line[1])
    #print(type(line[0]))
    if line != '':
        currentKey=",".join([line[0],line[1]])
        print(currentKey)   
        count = int(line[2])

        if lastKey == currentKey:
            currentCount += count
        else:
            if lastKey:
                print('(%s,%d)' %(lastKey, currentCount))
            currentCount = count
            lastKey = currentKey

if lastKey == currentKey:
    print((lastKey, currentCount))


# In[ ]:




