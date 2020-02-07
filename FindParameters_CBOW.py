#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Word2Vec - CBOW model 
# Parameters (size, window) 찾기

# Word2Vec을 위한 라이브러리 
from gensim.models import Word2Vec
# 한국어 처리
from konlpy.tag import Kkma
from konlpy.utils import pprint
# 그래프 표현하기 (고차원을 저차원으로 표현해주는 그래프)
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl
import matplotlib.pyplot as plt
import gensim.models as g
import matplotlib.font_manager as fm
# Warnings문 나오는 거 방지용
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

# 한국어 깨짐 방지 위해 한국어 폰트 설정
font_location = 'C:\Windows\\Fonts\\batang.ttc'
font_name = font_manager.FontProperties(fname=font_location).get_name()
rc('font', family=font_name)
# 글자 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

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
# size: number of dimensions of the embeddings (default = 100)
# window: target word와 target word 주변 단어 간의 최대 거리 (default = 5)
# min_count: 단어 빈도 수가 이 값보다 작으면 무시됨 (default = 5) 
# workers: numbers of partitions during training (default = 3)

for s in range (100, 350, 50):
    for w in range(3, 10):
        minCount = 10
        cbow_model = Word2Vec(data, min_count = minCount, iter = 5, size = s, window = w)

        cbow_model.save('CBOWFile')
        print("size = %d" %s)
        print("window = %d" %w)

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
        #print(df)

        # 그래프 그리기
        fig = plt.figure()
        fig.set_size_inches(40, 20)
        ax = fig.add_subplot(1 , 1,1)
        ax.scatter(df['x'], df['y'])
        for word, pos in df.iterrows():
            ax.annotate(word, pos, fontsize=30)
        plt.show()
        
file.close()


# In[ ]:





# In[ ]:




