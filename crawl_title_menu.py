#!/usr/bin/env python
# coding: utf-8

# In[15]:


# test 2
# melon 메인 chart 노래 제목 / 가수 텍스트로 출력하기

from selenium import webdriver

# path = 로컬에 저장된 chromedriver 위치
# url = 접속하려는 웹 페이지 주소
path = '/Users/mttw2820/Desktop/Mac/webCrawling/chromedriver'
url = 'https://melon.com/chart/index.htm'
driver = webdriver.Chrome(path)
driver.get(url)

# 차트 위치 잡기
# 태그이름[@속성 = '특정속성값'] 으로 지정한다
# 태그 내부 정보들은 get_attribute로 추출할 수 있다.
title = driver.find_element_by_xpath("//a[@class='mlog']")
menu = driver.find_elements_by_xpath("//div[@id='gnb_menu']/ul/*")
print("멜론 제목 출력 >> ")
print(title.get_attribute('title') + '\n')
print("사이트 메뉴 출력 >> ")
for m in menu :
    span = m.find_elements_by_tag_name('span')
    text = span[1].text
    print(text)
    


# In[ ]:




