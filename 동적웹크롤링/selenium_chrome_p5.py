from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import os

# Desktop 경로 설정
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
print(desktop)

# 키워드 및 크롤링 설정
Keyword = input('1. 수집 검색어는 무엇입니까?: ')
ArticleNum = int(input('2. 몇 건을 수집하시겠습니까?: '))

# 저장 파일 이름 및 경로 설정
txt_name = os.path.join(desktop, input('3.결과를 저장할 txt형식의 파일명을 쓰세요(예: 파일명.txt): '))
excel_name = os.path.join(desktop, input('4.결과를 저장할 xlsx형식의 파일명을 쓰세요(예: 파일명.xlsx): '))

# 기존 TXT 파일 초기화
with open(txt_name, 'w', encoding='utf-8') as f:
    f.write("")

# Selenium 초기 설정
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5) 

# 구글 열기
driver.get('https://www.google.com')

# 구글 검색. 검색어 입력 및 엔터
search_box = driver.find_element(By.NAME, 'q')  # Google 검색창의 이름 속성은 'q'
search_box.send_keys(Keyword)
search_box.send_keys(Keys.RETURN)

# 결과 저장 리스트 초기화
sn2 = []
title2 = []
url2 = []
site_name2 = []
snippet2 = []
banner_links2 = []
no = 1

print("데이터 수집을 시작합니다...")

# 스크롤 반복
while len(title2) < ArticleNum:
    # 현재 페이지 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('a[jsname="UWckNb"]')  # 구글 검색 결과 블록

    # 기사 수집
    for article in articles:
        if no > ArticleNum:
            break
        try:
            title = article.select_one('h3').text.strip()  # 제목
            a_tag = article.select_one('a')  # url; 메서드 호출
            url = a_tag['href']  # url; 'href' 속성 접근
            site_name = article.select_one('div.yuRUbf a').text.strip()  # 사이트 이름
            snippet = article.select_one('div.IsZvec').text.strip()  # 요약된 글
            banners = [link.text.strip() for link in article.select('div.eFM0qc a')]  # 배너 링크 텍스트
        except (AttributeError, KeyError):
            continue

print(url)
