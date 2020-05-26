#!/usr/bin/env python
# coding: utf-8

# In[19]:


# TF-IDF: 쓸 수 없는 방식일 듯

import pandas as pd
from math import log10
#from sklearn.feature_extraction.text import TfidfVectorizer

def f(t,d):
    return d.count(t)
def tf(t,d):
    return 0.5 + 0.5*f(t,d)/max([f(w,d) for w in d])
def idf(t, D):
    numerator = len(D)
    denominator = 1 + len([True for d in D if t in d])
    return log10(numerator/denominator)
def tfidf(t, d, D):
    return tf(t, d) * idf(t, D)
def tokenizer(d):
    return d.split()
def tfidfScorer(D):
    tokenized_D = [tokenizer(d) for d in D]
    result = []
    for d in tokenized_D:
        result.append([(t, tfidf(t,d,tokenized_D)) for t in d])
    return result
file = open("tagList_d3_fTimelist.txt", "r", encoding="UTF-8")
data = []
temp = []
while True:
    line = file.readline()
    if not line: break
    line = line.rstrip('\n')
    temp.append(line)

for t in temp:
    data.append(t)

for i, doc in enumerate(tfidfScorer(data)):
    print(doc)

# Sklearn 이용하면
'''
tfidfv = TfidfVectorizer().fit(data)
print(tfidfv.fit_transform(data).toarray())
print(tfidfv.vocabulary)
'''


# In[ ]:




