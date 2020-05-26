#!/usr/bin/env python
# coding: utf-8

# In[25]:


#Word2Vec 기본 예제 (영어!! 한국어는 꼭 konlpy 써야 함!!)

from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
#define training data
'''sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
            ['this','is','the','second', 'sentence'],
            ['yet', 'another', 'sentence'],
            ['one', 'more', 'sentence'],
            ['and', 'the', 'final', 'sentence']]'''
sentences = [['man', 'king'],
             ['woman', 'queen'],
             ['man', 'uncle'],
             ['woman', 'aunt'],
             ['aunt', 'queen'],
             ['uncle', 'king']
            ]
#train model
model = Word2Vec(sentences, min_count = 1)
'''
#summarize the loaded model
print(model)

#summarize vocabulary
words = list(model.wv.vocab)
print(words)

#access vector for one word
print(model['sentence'])
#save model
model.save('model.bin')
#load model
new_model = Word2Vec.load('model.bin')
print(new_model)'''

X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()


# In[ ]:




