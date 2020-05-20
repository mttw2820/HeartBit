#!/usr/bin/env python
# coding: utf-8

# In[1]:


# K-Means
# Word2Vec - CBOW model (Specific version) 

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
get_ipython().run_line_magic('matplotlib', 'inline')
import gensim.models as g
import matplotlib.font_manager as fm
# K-means 라이브러리
from sklearn.cluster import KMeans
# Warnings문 나오는 거 방지용
import warnings
warnings.filterwarnings("ignore")
from scipy.spatial import distance
import pandas as pd
import re
import operator

# 한국어 깨짐 방지 위해 한국어 폰트 설정
font_location = 'C:\Windows\\Fonts\\batang.ttc'
font_name = font_manager.FontProperties(fname=font_location).get_name()
rc('font', family=font_name)
# 글자 깨짐 방지
mpl.rcParams['axes.unicode_minus'] = False


# In[2]:


file = open("tagList_d5.txt", "r", encoding="UTF-8")

data = []

# 한 줄씩 읽기
temp = []  
while True:
    line = file.readline()
    if not line: break
    temp.append(line)

# 이중리스트에 저장하기 
for t in temp:
    data.append(t.split())

# 리스트에 저장하기(빈도수 셀 때 필요)
data_list = []
for dl in data:
    for dll in dl:
        data_list.append(dll)
        
# 단어 별 빈도수 세기
frequency = {}

for word in data_list:
    count = frequency.get(word,0)
    frequency[word] = count + 1
     
frequency_list = frequency.keys()
total_average = 0

# 빈도수가 일정 수준 이상이면 보관(store)
store = {}
a =50
for words in frequency_list:
    total_average = total_average + frequency[words]
    if (frequency[words] >= a):
        store[words] = frequency[words]
        #print(words, frequency[words])
        
# 특정 단어 있는지 확인하기
wantToSearch = '여름밤'
if (wantToSearch in frequency):
    print(wantToSearch, "의 빈도수: ", frequency.get(wantToSearch))
print("총 단어 수: ", total_average)
print("단어 종류: ", len(frequency_list))


# 단어 빈도수의 평균값
print("단어 빈도수의 평균: ", total_average/len(frequency_list))


print("*",a, "이상의 단어 수: ", len(store))
print(store)


# In[4]:


# CBOW model
# size: number of dimensions of the embeddings (default = 100)
# window: target word와 target word 주변 단어 간의 최대 거리 (default = 5)
# min_count: 단어 빈도 수가 이 값보다 작으면 무시됨 (default = 5) 
# workers: numbers of partitions during training (default = 3)


minCount = 20
s = 250
w = 6
#cbow_model = Word2Vec(data, min_count = minCount, iter = 5, size = s, window = w)

#cbow_model.save('CBOWModelFile')
print("size = %d" %s)
print("window = %d" %w)

cModel = g.Doc2Vec.load('CBOWModelFile')
#vocab = list(cModel.wv.vocab)
vocab = list(cbow_model.wv.vocab)
print("CBOW 모델에 의해 뽑힌 단어 수: ", len(vocab))


# In[70]:


cModel = g.Doc2Vec.load('CBOWModelFile')
vocab = list(cModel.wv.vocab)
X = cModel[vocab]

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




# In[71]:


print(df)
data_points = df.values
#print(data_points)


# In[72]:


# 적합한 k 찾기 그래프
sse = {}
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(data_points)
    #df["cluster_id"] = kmeans.labels_
    sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
plt.figure()
plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
print(sse)
plt.show()


# In[73]:


import seaborn as sns

# K-mean clustering
kmeans = KMeans(n_clusters=5).fit(data_points)
#kmeans.labels_
df['cluster_id'] = kmeans.labels_
centroids = kmeans.cluster_centers_
print(centroids)


# In[109]:


sns.lmplot('x','y',data=df, fit_reg = False, scatter_kws={"s":180}, hue = "cluster_id")

count = 0
group0 = {}
group1 = {}
group2 = {}
group3 = {}
group4 = {}
#print(df.index)
# centroid와 그 그룹에 속한 점 간의 거리 계산하기
count = 0
for points in df['cluster_id']:
    if (points == 0):
        group0[df.index[count]] = distance.euclidean(centroids[0], data_points[count])
        #print(data_points[count])
    elif (points == 1):
        group1[df.index[count]] = distance.euclidean(centroids[1], data_points[count])
    elif (points == 2):
        group2[df.index[count]] = distance.euclidean(centroids[2], data_points[count])
    elif (points == 3):
        group3[df.index[count]] = distance.euclidean(centroids[3], data_points[count])
    elif (points == 4):
        group4[df.index[count]] = distance.euclidean(centroids[4], data_points[count])
    count = count+1
'''    
print(count)
print(group0)
print(group1)
print(group2)
print(group3)
print(group4)
'''



# In[75]:



# 빈도수로 필요한 정보만 얻기
def useful(dict):
    i = 0
    count_i = 0
    # itemgetter(1)이면 value값을 중심으로 정렬. 0이면 key 값을 중심으로 정렬
    
    while True:
        key_word = sorted(dict.items(), key= operator.itemgetter(1))[i]
        if (key_word[0] in store):
            print(key_word)
            print("빈도수: ", store.get(key_word[0]))
            count_i = count_i + 1
            if (count_i != 3):
                #key_word = sorted(dict.items(), key= operator.itemgetter(1))[i]
                i = i +1
            else:
                break
        else:
            i = i + 1
                #key_word = sorted(dict.items(), key= operator.itemgetter(1))[i]
    print("------------------------------------------------------")
    
       
    


# In[76]:


#print(sorted(group0.items(),key=operator.itemgetter(1)))
print("group0: ")
useful(group0)
#print("-----------------------------------------------------")
#print(sorted(group1.items(),key=operator.itemgetter(1)))
print("group1: ")
useful(group1)
#print(sorted(group2.items(),key=operator.itemgetter(1)))
#print("-----------------------------------------------------")
print("group2 ")
useful(group2)
#print(sorted(group3.items(),key=operator.itemgetter(1)))
#print("-----------------------------------------------------")
print("group3 ")
useful(group3)
#print("-----------------------------------------------------")
print("group4 ")
# print(sorted(group4.items(),key=operator.itemgetter(1)))
useful(group4)


# In[119]:


# 그룹 내에서 또 자르기
def specific(groupNumber, groupK):
    group_list = df[df.cluster_id == groupNumber]
    i = 0
    #print(len(group_list))
    #print(group_list)

    # x와 y만 가져오기
    #print(group1_list[['x', 'y']])

    # group_list는 df와 같은 역할, group_points는 data_points와 같은 역할 
    # group_list는 단어와 함께 행, 열 형태로 나옴, group_points는 리스트 형태로 나옴
    group_list = group_list[['x', 'y']]
    group_points = group_list.values
    #print(group_points)

    # K-means
    smallKmeans = KMeans(n_clusters=groupK).fit(group_points)
    group_list['small_id'] = smallKmeans.labels_
    sCentroids = smallKmeans.cluster_centers_
    print(sCentroids)
    #print(group_list)
    sns.lmplot('x','y',data=group_list, fit_reg = False, scatter_kws={"s":180}, hue = "small_id")
    
    basket = {}
    group_s0 = {}
    group_s1 = {}
    group_s2 = {}
    group_s3 = {}
    group_s4 = {}
    
    # 작은 cluster의 centroid와 그 그룹에 속한 점 간의 거리 계산하기
    smallCount = 0
    for points in group_list['small_id']:
        if (points == 0):
            group_s0[group_list.index[smallCount]] = distance.euclidean(sCentroids[0], group_points[smallCount])
        elif (points == 1):
            group_s1[group_list.index[smallCount]] = distance.euclidean(sCentroids[1], group_points[smallCount])   
        elif (points == 2):
            group_s2[group_list.index[smallCount]] = distance.euclidean(sCentroids[2], group_points[smallCount])   
        elif (points == 3):
            group_s3[group_list.index[smallCount]] = distance.euclidean(sCentroids[3], group_points[smallCount])
        elif (points == 4):
            group_s4[group_list.index[smallCount]] = distance.euclidean(sCentroids[4], group_points[smallCount])

        smallCount = smallCount+1
        
    # 편리하게 사용하기 위해 이중 딕셔너리 사용
    basket['Small group 0'] = group_s0
    basket['Small group 1'] = group_s1
    basket['Small group 2'] = group_s2
    basket['Small group 3'] = group_s3
    basket['Small group 4'] = group_s4
    # print(basket)
    for g in basket:
        if len(basket[g]) != 0:
            useful(basket[g])
    
    #useful(group_s0)
    #useful(group_s1)
    #useful(group_s2)
    #useful(group_s3)
    #useful(group_s4)


# In[120]:


# 그룹 내에서 자르기 결과
specific(0, 2)
#specific(1, 5)
specific(2, 2)
#specific(3, 2)
#specific(4, 5)


# In[223]:


# 단어 주위에 있는 단어 추출하기
def CloseWord(wantWord):
    # 찾는 단어의 좌표 저장
    word_x = df.loc[wantWord]['x']
    word_y = df.loc[wantWord]['y']
    word_group = df.loc[wantWord]['cluster_id']
    word_loc = (word_x, word_y)
    print(word_loc)
    
    group_list = df[df.cluster_id == word_group]
    i = 0
    #print(len(group_list))
    #print(group_list)
    
    # group_list는 df와 같은 역할, group_points는 data_points와 같은 역할 
    # group_list는 단어와 함께 행, 열 형태로 나옴, group_points는 리스트 형태로 나옴
    group_list = group_list[['x', 'y']]
    group_points = group_list.values
    #print(group_points)
    
    
    distance_info = {}
    # 작은 cluster의 centroid와 그 그룹에 속한 점 간의 거리 계산하기
    count = 0
    #print(group_points[0])
    for points in group_points:
        dis = distance.euclidean(word_loc, points)
        if (dis != 0):
            distance_info[group_list.index[count]] = dis
        count = count + 1
    print(distance_info)  
    useful(distance_info)


# In[224]:


CloseWord('조용한')


# In[195]:


#단어의 x, y, cluster_id 추출
print(df.loc['여름밤'])


# In[132]:


# 적합한 k 찾기 함수
def appropriateK(groupNumber):
    sse = {}
    group_list = df[df.cluster_id == groupNumber]
    for k in range(1, 10):
        group_list = group_list[['x', 'y']]
        group_points = group_list.values
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(group_points)
        #df["cluster_id"] = kmeans.labels_
        sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
    plt.figure()
    plt.plot(list(sse.keys()), list(sse.values()))
    plt.xlabel("Number of cluster")
    plt.ylabel("SSE")
    print(sse)
    plt.show()


# In[133]:


appropriateK(4)


# In[196]:


file.close()


# In[ ]:




