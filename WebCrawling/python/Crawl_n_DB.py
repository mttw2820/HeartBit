
# coding: utf-8

# In[4]:

# melon 태그 검색 후 상위 플레이리스트 4개의 음악 리스트 DB에 저장

from selenium import webdriver
import sqlite3

# path = 로컬에 저장된 chromedriver 위치
# url = 접속하려는 웹 페이지 주소
path = './chromedriver.exe'
url = 'https://www.melon.com/dj/themegenre/djthemegenre_list.htm'
driver = webdriver.Chrome(path)
driver.get(url)
driver.implicitly_wait(10)
db = "./MelonMusicDatabase.db"


# In[5]:

# TAG 정보 DB에 저장
# 한번만 실행하면 되니까 다시 실행하지 말기!!

tag_group0 = ["데이트", "달달한", "썸", "고백", "인디음악", "연인", "봄", "힘들때", "응원", "연애", "달달", "어쿠스틱", "산책", "센치"]
tag_group1 = ["행복", "고요한", "밤새벽", "감성인디", "분위기깡패", "밤에듣기좋은노래", "조용한", "집", "가을감성", "여행산책", "토닥토닥"]
tag_group2 = ["주말", "편안한", "커피", "뉴에이지", "피아노", "아침", "재즈", "오후", "연주곡", "클래식", "자장가", "모닝콜", "노동요", "출근길", "집중", "잠들기전", "공부", "독서"]
tag_group3 = ["여름", "명곡", "신나는", "알앤비", "여행", "팝", "아이돌", "클럽", "트렌디", "댄스", "운동", "매장음악", "EDM", "스트레스"]
tag_group4 = ["새벽", "분위기", "드라이브", "눈물", "겨울", "비", "밤", "발라드", "우울", "힐링", "감성", "사랑", "이별", "슬픔", "휴식", "기분전환", "잔잔한"]
tag_groups = [tag_group0, tag_group1, tag_group2, tag_group3, tag_group4]

# 태그 DB에 저장
for i in range(5) :
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    for tags in tag_groups[i] :
        sql = "insert into TagData(groupNum, tagName) values (?, ?)"
        cur.execute(sql, (i, tags))
    
    conn.commit()
    conn.close()


# In[ ]:




# In[6]:

# DB에 음악 정보 저장/출력
# 한 플레이스트 첫 페이지의 음악정보 추출
def crawl_musiclist(group_num, tag_num) :
    musicList = driver.find_elements_by_xpath("//tbody//tr")
    titleList = driver.find_elements_by_xpath("//div[@class='ellipsis rank01']")
    singerList = driver.find_elements_by_xpath("//div[@class='ellipsis rank02']")
    
    total = len(musicList)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = "insert into MusicData(searchTag, title, singer) values(?, ?, ?)"
    for index in range(total) :
        # 음악 각각의 제목과 가수이릉을 텍스트로 추출
        musicTitle = titleList[index].find_element_by_tag_name('span').find_element_by_tag_name('a').text
        try :
            singer = singerList[index].find_element_by_tag_name('a').text
        except Exception as e:
            print(e)
            singer = "NULL"
        cur.execute(sql, (tag_num, musicTitle, singer))
        print(musicTitle, singer)
    conn.commit()
    conn.close()
        
    
        

# 플레이리스트 정보 추출
def crawl_playlist(group_num, tag_num) :
    listInfo = driver.find_elements_by_xpath("//h5[@class='title']")[1]
    listSize = listInfo.find_element_by_tag_name('span').text
    



    
# 모든 태그에 대해서 크롤링
conn = sqlite3.connect(db)
cur = conn.cursor()
query = "select * from TagData"
cur.execute(query)
all_tags_in_db = cur.fetchall()
cur.close()

for tag in all_tags_in_db :
    # 태그 검색
    # 태그이름 [@속성 = '특정속성값'] 으로 지정
    # 태그 내부 정보들은 get_attribute로 추출할 수 있다.
    search = driver.find_element_by_xpath("//div[@class='input_wrap']")
    search_tag = search.find_element_by_tag_name('input')
    search_btn = search.find_element_by_tag_name('button')
    
    group_num = tag[0]
    tag_num = tag[1]
    tag_name = tag[2]
    
    search_tag.clear()
    search_tag.send_keys(tag_name)
    search_btn.click()
    
    print(tag_num, tag_name)

    # 상위 4개 플레이리스트 크롤
    for x in range(4) :
        playlist = driver.find_elements_by_xpath("//div[@class='entry']")
        plist = playlist[x]
        # 플레이리스트 가져오기
        List = plist.find_elements_by_tag_name('a')[1]
        #listName = List.text
        #print(listName)
        List.click()
        crawl_musiclist(group_num, tag_num)
        driver.execute_script("window.history.go(-1)")
    
print("over")


# In[3]:

# clear DB
# 실행하면 DB 날라가니까 주의

conn = sqlite3.connect(db)
cur = conn.cursor()

delete_sql_for_TagData = "DELETE FROM TagData"
delete_sql_for_MusicData = "DELETE FROM MusicData"
update_sq_zero_TagData = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'TagData'"
update_sq_zero_MusicData = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'MusicData'"
cur.execute(delete_sql_for_TagData)
cur.execute(delete_sql_for_MusicData)
cur.execute(update_sq_zero_TagData)
cur.execute(update_sq_zero_MusicData)

conn.commit()
conn.close()


# In[ ]:



