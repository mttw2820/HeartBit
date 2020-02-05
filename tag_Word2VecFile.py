#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Word2Vec - CBOW model, Skip Gram model 
# size, window 적절한 값 찾기

# window: 주어진 단어를 어느 정도 포함하여 계산할 것인지를 나타냄. (보통 10개의 단어가 있으면 window를 5로 설정하는게 일반적이다)
# size: dimensionality of vector - 단어 수보다 너무 높게 잡으면 overfitting의 가능성 있음 

# Word2Vec을 위한 라이브러리 
from gensim.models import Word2Vec
# 한국어 처리
from konlpy.tag import Kkma
from konlpy.utils import pprint
# 나중에 파일 넣을 때 필요한 import
#from gensim.test.utils import common_texts, get_tmpfile
# 그래프 그리기
from sklearn.decomposition import PCA
from matplotlib import pyplot
import matplotlib.font_manager as fm
# Warnings문 나오는 거 방지용
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
#data가 파일 형태일 경우
#path = get_tmpfile("")
#model = Word2Vec(common_texts, size = 100, window = 5, min_count = 1)
#model.save("word2vec.model")
#OR
#path = open('파일명')
#p = path.read()

file = open("tagList_d3_fTimelist.txt", "r", encoding="UTF-8")

data = []

# 한 줄씩 읽기
temp = []  
while True:
    line = file.readline()
    if not line: break
    temp.append(line)

# 리스트에 저장하기 
for t in temp:
    data.append(t.split())
#print(data)

# 단어 하나씩 추출하기
word = []
for d in data:
    for da in d:
        word.append(da)
#print(word)
print(len(word))
word = set(word)
#print(word)
print(len(word))

# CBOW model
print("CBOW:")
cbow_model = Word2Vec(data, min_count = 10, size = 80, window = 16000, iter = 5)
#print(cbow_model)


# 유사도 비교하기
#print("\n단어 간 코사인 값 비교:")
#print ("Cosine similarity between 기분좋은 - 행복: ", cbow_model.similarity("기분좋은", "행복"))
#print ("Cosine similarity between 설렘 - 사랑: ", cbow_model.similarity("설렘", "사랑"))
### 한 단어 주어지면 가장 가까운 단어 보여주기
sample = '신나는'
print("\n'" + sample + "' 단어와 유사도 높은 순서: ")
print(cbow_model.wv.most_similar(positive=sample, topn = 30))


# 개별 벡터 보여주기 
print("\n각각 단어의 벡터값: ")
#for w in word:
#    print(w, cbow_model.wv.word_vec(w))

cbow_model.save('CBOWFile')
print('\n---------------------------------------------------------------')

'''

# Skip Gram model
print("Skip Gram:\n")
skip_model = Word2Vec(data, min_count = 1, size = 5, window = 10, iter = 5, sg = 1)

# Skip Gram의 유사도 비교하기
print("\n단어 간 코사인 값 비교:")
print ("Cosine similarity between '행복'- 기쁨: ", skip_model.similarity("행복", "기쁨"))
print ("Cosine similarity between '설렘'- 사랑: ", skip_model.similarity("설렘", "사랑"))
### 한 단어 주어지면 가장 가까운 단어 보여주기
print("\n'스트레스' 단어와 유사도 높은 순서: ")
sample = '스트레스'
print(skip_model.wv.most_similar(positive=sample))

# 개별 벡터 보여주기 
print("\n각각 단어의 벡터값: ")
store_skip = skip_model.wv
for w in word:
    print(w, store_skip.word_vec(w))



print('\n---------------------------------------------------------------')
'''

file.close()


# In[5]:


# T-SNE 사용 (고차원을 저차원으로 표현해주는 그래프)
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl
import matplotlib.pyplot as plt
import gensim.models as g
import matplotlib.font_manager as fm

# 한국어 깨짐 방지 위해 한국어 폰트 설정
font_location = 'C:\Windows\\Fonts\\batang.ttc'
font_name = font_manager.FontProperties(fname=font_location).get_name()
rc('font', family=font_name)
# 글자 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

store_model = g.Doc2Vec.load('CBOWFile')
vocab = list(store_model.wv.vocab)


X = store_model[vocab]

# 이차원 그래프로 표현
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
#print(len(X_tsne))

# 표 그리기
df = pd.DataFrame(X_tsne, index = vocab[:], columns=['x','y'])
df.shape
print(df)

# 그래프 그리기
fig = plt.figure()
fig.set_size_inches(40, 20)
ax = fig.add_subplot(1 , 1,1)
ax.scatter(df['x'], df['y'])
for word, pos in df.iterrows():
    ax.annotate(word, pos, fontsize=30)
plt.show()


# In[ ]:




