#!/usr/bin/env python
# coding: utf-8

# In[7]:


# pytorch 예제
import torch
import torch.nn as nn     #for word embeddings
import torch.nn.functional as F
import torch.optim as optim
torch.manual_seed(1)

word_to_ix = {"":0, "바나나": 1}
embeds = nn.Embedding(2,5)    #2 words in vocab, 5 dimensional embeddings
lookup_tensor = torch.tensor([word_to_ix["사과"]], dtype=torch.long)
hello_embed = embeds(lookup_tensor)
print(hello_embed)


# In[23]:


Context_size = 2
raw_text = """hi apple banana sleep""".split()
vocab = set(raw_text)
print(vocab)
vocab_size = len(vocab)
print(vocab_size)


# In[26]:


word_to_ix = {word: i for i, word in enumerate(vocab)}
print(word_to_ix)

data = []
for i in range(0, len(raw_text) - 2):
    context = [raw_text[i - 2], raw_text[i - 1],
               raw_text[i + 1], raw_text[i + 2]]
    target = raw_text[i]
    data.append((context, target))
print(data)


# In[ ]:




