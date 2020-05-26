#!/usr/bin/env python
# coding: utf-8

# In[39]:


# Word2Vec - CBOW model, Skip Gram model (미완성-그래프 적용은 미완)

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

data = [
    ['잔잔한', '조용한', '고요한', '감성', '휴식', '힐링', '새벽', '밤', '기분전환', '카페'],
    ['밤새벽','밤', '잔잔한', '감성', '휴식', '힐링', '이별', '추억', '발라드', '사랑'],
    ['신나는', '기분전환', '드라이브', '여행', '스트레스', '댄스', '여름', '감성', '휴식', '사랑'],
    ['모닝콜', '아침', '집중', '출근길', '노동요', '피아노', '카페', '클래식', '주말', '자장가'],
    ['고요한', '잔잔한', '밤', '새벽','휴식', '카페', '감성', '발라드', '조용한', '힐링'], 
    ['아침', '모닝콜', '기분전환', '출근길', '카페', '드라이브', '잔잔한', '감성', '힐링', '스트레스'],
    ['드라이브', '기분전환', '여행', '신나는', '감성', '스트레스', '휴식', '카페', '운동', '힐링'],
    ['스트레스', '기분전환','드라이브','신나는','운동', '여름', '여행', '노동요']
]


# 단어 하나씩 추출하기
word = []
for d in data:
    for da in d:
        word.append(da)
#print(word)
#print(len(word))
word = set(word)
#print(word)
#print(len(word))

# CBOW model
print("CBOW:")
cbow_model = Word2Vec(data, min_count = 1, size = 5, window = 10, iter = 5)
#print(cbow_model)


# 유사도 비교하기
print("\n단어 간 코사인 값 비교:")
print ("Cosine similarity between '잔잔한'- 고요한: ", cbow_model.similarity("잔잔한", "고요한"))
print ("Cosine similarity between '잔잔한'- 모닝콜: ", cbow_model.similarity("잔잔한", "모닝콜"))
### 한 단어 주어지면 가장 가까운 단어 보여주기
print("\n'스트레스' 단어와 유사도 높은 순서: ")
sample = '스트레스'
print(cbow_model.wv.most_similar(positive=sample))


# 개별 벡터 보여주기 
print("\n각각 단어의 벡터값: ")
store_cbow = cbow_model.wv
for w in word:
    print(w, store_cbow.word_vec(w))

print('\n---------------------------------------------------------------')


# Skip Gram model
print("Skip Gram:\n")
skip_model = Word2Vec(data, min_count = 1, size = 5, window = 10, iter = 5, sg = 1)

# Skip Gram의 유사도 비교하기
print("\n단어 간 코사인 값 비교:")
print ("Cosine similarity between '잔잔한'- 고요한: ", skip_model.similarity("잔잔한", "고요한"))
print ("Cosine similarity between '잔잔한'- 모닝콜: ", skip_model.similarity("잔잔한", "모닝콜"))
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


# In[56]:


# 그래프 그리기
# https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
'''
import seaborn as sns
print("CBOW: ")
vocab = cbow_model.wv.vocab
x = cbow_model[vocab]
pca = PCA(n_components=5)
result1 = pca.fit_transform(x)

DF1 = pd.DataFrame(data=result1, columns = ['Vector 1', 'Vector 2', 'Vector 3', 'Vector 4', 'Vector 5'])

sns.pairplot(DF1)
plt.show()'''


# In[ ]:




