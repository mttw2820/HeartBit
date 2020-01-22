#!/usr/bin/env python
# coding: utf-8

# In[1]:


# melon 태그 테마장르 추천에 검색하기

from selenium import webdriver

# path = 로컬에 저장된 chromedriver 위치
# url = 접속하려는 웹 페이지 주소
path = '/Users/mttw2820/Desktop/Mac/webCrawling/chromedriver'
url = 'https://www.melon.com/dj/themegenre/djthemegenre_list.htm'
driver = webdriver.Chrome(path)
driver.get(url)

# 차트 위치 잡기
# 태그이름[@속성 = '특정속성값'] 으로 지정한다
# 태그 내부 정보들은 get_attribute로 추출할 수 있다.
search = driver.find_element_by_xpath("//div[@class='input_wrap']")
search_tag = search.find_element_by_tag_name('input')
search_btn = search.find_element_by_tag_name('button')
tag = "휴식"
search_tag.clear()
search_tag.send_keys(tag)
search_btn.click()

# tag에 들어간 검색어의 검색 결과가 나온다


# In[ ]:




