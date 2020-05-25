#!/usr/bin/env python
# coding: utf-8

# In[11]:


# K-Means: 최종 파일
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

# 빈도수가 일정 수준 이상이면 보관(store): 여기서는 20 이상이면 유효하다 봄
store = {}
a =20
for words in frequency_list:
    total_average = total_average + frequency[words]
    if (frequency[words] >= a):
        store[words] = frequency[words]
        #print(words, frequency[words])
        
# 특정 단어 있는지 확인하기
#wantToSearch = '여름밤'
#if (wantToSearch in frequency):
#    print(wantToSearch, "의 빈도수: ", frequency.get(wantToSearch))
print("총 단어 수: ", total_average)
print("단어 종류: ", len(frequency_list))


# 단어 빈도수의 평균값
print("단어 빈도수의 평균: ", total_average/len(frequency_list))


print(a, "이상의 단어 종류 수: ", len(store))
store_total = 0
for s in store:
    if (s in frequency):
        store_total = store_total+ frequency[s]
# print(len(store))
print(a,"이상의 단어 총수:", store_total)

# Word2Vec 적용하기
# CBOW model
# size: number of dimensions of the embeddings (default = 100)
# window: target word와 target word 주변 단어 간의 최대 거리 (default = 5)
# min_count: 단어 빈도 수가 이 값보다 작으면 무시됨 (default = 5) 
# workers: numbers of partitions during training (default = 3)


minCount = 20
s = 250
w = 6
cbow_model = Word2Vec(data, min_count = minCount, iter = 5, size = s, window = w)

cbow_model.save('CBOWModelFile')
print("size = %d" %s)
print("window = %d" %w)

cModel = g.Doc2Vec.load('CBOWModelFile')
vocab = list(cModel.wv.vocab)



# 좌표평면 상에 그리기
cModel = g.Doc2Vec.load('CBOWModelFile')
vocab = list(cModel.wv.vocab)
X = cModel[vocab]

# 이차원 그래프로 표현: t-SNE
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





# 태그와 2차원 좌표로 표현된 데이터
print("< 2차원으로 표현 >")
print(df)
data_points = df.values
#print(data_points)

# 적합한 k 찾기 그래프:SSE
print("< SSE >")
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

import seaborn as sns

# 그룹 내 centroid 계산하기
# K-mean clustering
kmeans = KMeans(n_clusters=5).fit(data_points)
#kmeans.labels_
df['cluster_id'] = kmeans.labels_
centroids = kmeans.cluster_centers_
print("< Centroids >")
print(centroids)

print("\n\n")
# K-means 그리기
sns.lmplot('x','y',data=df, fit_reg = False, scatter_kws={"s":180}, hue = "cluster_id")

count = 0
# 거리 + 빈도수 보관하는 공간
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
        group0[df.index[count]] = [distance.euclidean(centroids[0], data_points[count]), frequency.get(df.index[count])]
        #print(frequency.get(df.index[count]))
    elif (points == 1):
        group1[df.index[count]] = [distance.euclidean(centroids[1], data_points[count]), frequency.get(df.index[count])]
    elif (points == 2):
        group2[df.index[count]] = [distance.euclidean(centroids[2], data_points[count]), frequency.get(df.index[count])]
    elif (points == 3):
        group3[df.index[count]] = [distance.euclidean(centroids[3], data_points[count]), frequency.get(df.index[count])]
    elif (points == 4):
        group4[df.index[count]] = [distance.euclidean(centroids[4], data_points[count]), frequency.get(df.index[count])]
    count = count+1






# 빈도수로 유효하다 생각되는 거 얻기: 3개만 얻기
def useful(dict):
    i = 0
    count_i = 0
    # itemgetter(1)이면 value값을 중심으로 정렬. 0이면 key 값을 중심으로 정렬
    #print(sorted(dict.items(), key = operator.itemgetter(1)))

    while True:
        key_word = sorted(dict.items(), key= operator.itemgetter(1))[i]
        #print(key_word)
       
        if (key_word[0] in store):
            print(key_word)
            #print("빈도수: ", store.get(key_word[0]))
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
    
       
    


# 빈도수로  전체 태그 정보 얻기: 상위에 위치할수록 centroid와 가까운 태그
def useful2(dict):
    i = 0
    count_i = 0
    # itemgetter(1)이면 value값을 중심으로 정렬. 0이면 key 값을 중심으로 정렬
    print(sorted(dict.items(), key = operator.itemgetter(1)))
    print("------------------------------------------------------")
    
       
    

# centroid와 가까운 순서로 배열하기
# 위의 3개 단어는 가까우면서 빈도수를 만족하는 단어(useful 함수)
# useful2 형태: 태그 이름 + centroid와의 거리 + 빈도수
#print(sorted(group0.items(),key=operator.itemgetter(1)))
print("< 결과물: 유사단어 최상위 3개 + (태그 이름 + [centroid와의 거리 + 빈도수]) >")
print("group0: ")
useful(group0)
useful2(group0)
#print("-----------------------------------------------------")
#print(sorted(group1.items(),key=operator.itemgetter(1)))
print("group1: ")
useful(group1)
useful2(group1)
#print(sorted(group2.items(),key=operator.itemgetter(1)))
#print("-----------------------------------------------------")
print("group2 ")
useful(group2)
useful2(group2)
#print(sorted(group3.items(),key=operator.itemgetter(1)))
#print("-----------------------------------------------------")
print("group3 ")
useful(group3)
useful2(group3)
#print("-----------------------------------------------------")
print("group4 ")
useful(group4)
useful2(group4)

file.close()


# In[ ]:




