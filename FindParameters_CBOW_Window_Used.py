#!/usr/bin/env python
# coding: utf-8

# In[124]:


# Word2Vec - CBOW model 
# Parameters (size, window) 중 window 찾기
# Window: 3~9까지 변화 

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

import math
from scipy.spatial import distance
# 한국어 깨짐 방지 위해 한국어 폰트 설정
font_location = 'C:\Windows\\Fonts\\batang.ttc'
font_name = font_manager.FontProperties(fname=font_location).get_name()
rc('font', family=font_name)
# 글자 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False

file = open("tagList_d5.txt", "r", encoding="UTF-8")

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


# 단어 하나씩 추출하기
word = []
for d in data:
    for da in d:
        word.append(da)
print("단어의 총 개수: ", len(word))
word = set(word)
print("단어의 unique한 값들의 개수: ", len(word))



# In[125]:


print("CBOW:")
# size: number of dimensions of the embeddings (default = 100)
# window: target word와 target word 주변 단어 간의 최대 거리 (default = 5)
# min_count: 단어 빈도 수가 이 값보다 작으면 무시됨 (default = 5) 
# workers: numbers of partitions during training (default = 3)

# euclidean distance와 cosine distance가 저장될 공간 준비하기
euc1 = []
euc2 = []
euc3 = []
euc4 = []
euc5 = []
euc6=  []
cos1 = []
cos2 = []
cos3 = []
cos4 = []
cos5 = []
cos6=  []

windowDetail = []                       # 다수결로 투표할 때 사용될 공간: 후보
result = []                             # 다수결로 투표할 때 사용될 공간: 투표결과 

# Window는 3~9까지 변화
for w in range (3, 10):
    print("\nwindow = %d" %w)
    
    # euclidean distance 초기 값 0
    dist1 = 0
    dist2 = 0
    dist3 = 0
    dist4 = 0
    dist5 = 0
    dist6 = 0
    # cosine distance 초기 값 0
    c_dist1 = 0
    c_dist2 = 0
    c_dist3 = 0
    c_dist4 = 0
    c_dist5 = 0
    c_dist6 = 0
    
    repeat = 0                                # size에 변화시켜준 횟수
    windowDetail.append(w)
    
    # size를 다양하게 반영시키며 접근(50~350까지 25씩 변경)
    for r in range(0, 5):
        repeat = repeat + 1
        minCount = 20
        cbow_model = Word2Vec(data, min_count = minCount, iter = 5, size = 100, window = w)

        cbow_model.save('CBOWFile')
        #print("\nsize = %d" %s)
        
        store_model = g.Doc2Vec.load('CBOWFile')
        vocab = list(store_model.wv.vocab)
        
        # 사용할 태그 
        s1 = '아침'
        s2 = '모닝콜'
        s3 = '잔잔한'
        s4 = '고요한'
        s5 = '카페'
        s6 = '휴식'
        # s7 = '운동'
        s8 = '클럽'
        s9 = 'EDM'
        s10 = '조용한'
        s11 = '여름'
        s12 = '추위'
        
        # 유사태그: 아침-모닝콜
        dist1 = distance.euclidean(store_model.wv.word_vec(s1),(store_model.wv.word_vec(s2))) + dist1
        c_dist1 = store_model.similarity(s1, s2) + c_dist1
        # 유사태그: 잔잔한-고요한
        dist2 = distance.euclidean(store_model.wv.word_vec(s3),(store_model.wv.word_vec(s4))) + dist2
        c_dist2 = store_model.similarity(s3, s4) + c_dist2
        # 유사태그: 카페-휴식
        dist3 = distance.euclidean(store_model.wv.word_vec(s5),(store_model.wv.word_vec(s6))) + dist3
        c_dist3 = store_model.similarity(s5, s6) + c_dist3
        # 상반태그: 아침-클럽
        dist4 = distance.euclidean(store_model.wv.word_vec(s1),(store_model.wv.word_vec(s8))) + dist4
        c_dist4 = store_model.similarity(s1, s8) + c_dist4
        # 상반태그: EDM-조용한
        dist5 = distance.euclidean(store_model.wv.word_vec(s9),(store_model.wv.word_vec(s10))) + dist5
        c_dist5 = store_model.similarity(s9, s10) + c_dist5
        # 상반태그: 여름-추위
        dist6 = distance.euclidean(store_model.wv.word_vec(s11),(store_model.wv.word_vec(s12))) + dist6
        c_dist6 = store_model.similarity(s11, s11) + c_dist6
    
    # window 동일하지만 변화를 준 size의 평균값 구하기
    euc1.append(dist1/repeat)
    euc2.append(dist2/repeat)
    euc3.append(dist3/repeat)
    euc4.append(dist4/repeat)
    euc5.append(dist5/repeat)
    cos1.append(c_dist1/repeat)
    cos2.append(c_dist2/repeat)
    cos3.append(c_dist3/repeat)
    cos4.append(c_dist4/repeat)
    cos5.append(c_dist5/repeat)

    print(s1, "- ", s2)    
    print(dist1/repeat)
    print(c_dist1/repeat)    
    print(s3, "- ", s4)    
    print(dist2/repeat)
    print(c_dist2/repeat)  
    print(s5, "- ", s6)    
    print(dist3/repeat)
    print(c_dist3/repeat)  
    print(s1, "- ", s8)    
    print(dist4/repeat)
    print(c_dist4/repeat)  
    print(s9, "- ", s10)    
    print(dist5/repeat)
    print(c_dist5/repeat)  


# In[126]:


# 어느 정도 범위에 있는 애들은 허용하기
def ok(x, list, x_location):
    result.append(x_location)
    for l in list:
        if (list == euc4 or list == euc5 or list == cos4 or list == cos5):
            '''if (abs(x-l) <= 0.15 and x != l):
                print("걸림")
                print("\ts = ", windowDetail[list.index(l)], " -> ", l)
            '''
        if (abs(x - l) <= 0.03  and x != l):
            print("\ts = ", windowDetail[list.index(l)], " -> ", l)
            result.append(windowDetail[list.index(l)])


# In[127]:


# 유사도가 높아야 되는 애들 출력하기
print(s1, "- ", s2)
print("Euc w = ", windowDetail[euc1.index(min(euc1))], " -> ", min(euc1))
ok(min(euc1),euc1, windowDetail[euc1.index(min(euc1))])
print("Cos w = ", windowDetail[cos1.index(max(cos1))], " -> ", max(cos1))
ok(max(cos1),cos1, windowDetail[cos1.index(max(cos1))])
print(s3, "- ", s4)
print("Euc w = ", windowDetail[euc2.index(min(euc2))], " -> ", min(euc2))
ok(min(euc2),euc2, windowDetail[euc2.index(min(euc2))])
print("Cos w = ", windowDetail[cos2.index(max(cos2))], " -> ", max(cos2))
ok(max(cos2),cos2, windowDetail[cos2.index(max(cos2))])
print(s5, "- ", s6)
print("Euc w = ", windowDetail[euc3.index(min(euc3))], " -> ", min(euc3))
ok(min(euc3),euc3, windowDetail[euc3.index(min(euc3))])
print("Cos w = ", windowDetail[cos3.index(max(cos3))], " -> ", max(cos3))
ok(max(cos3),cos3, windowDetail[cos3.index(max(cos3))])

# 유사도가 낮아야 되는 애들 출력하기
print(s1, "- ", s8)
print("Euc w = ", windowDetail[euc4.index(max(euc4))], " -> ", max(euc4))
ok(max(euc4), euc4, windowDetail[euc4.index(max(euc4))])
print("Cos w = ", windowDetail[cos4.index(min(cos4))], " -> ", min(cos4))
ok(min(cos4), euc4, windowDetail[cos4.index(min(cos4))])
print(s9, "- ", s10)
print("Euc w = ", windowDetail[euc5.index(max(euc5))], " -> ", max(euc5))
ok(max(euc5), euc5, windowDetail[euc5.index(max(euc5))])
print("Cos w = ", windowDetail[cos5.index(min(cos5))], " -> ", min(cos5))
ok(min(cos5), euc5,windowDetail[cos5.index(min(cos5))])
file.close()


# In[128]:


result_count = []
final = {}

# print(result)
result.sort()

for w in windowDetail:
    #result.count(w)
    result_count.append(result.count(w))
    #final[windowDetail(w)] = result_count(w)
print("[3, 4, 5, 6, 7, 8, 9]")
print(result_count)


# In[17]:


file.close()


# In[ ]:




