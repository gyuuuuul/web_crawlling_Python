from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# 검색할 키워드 입력
query = input('검색할 키워드를 입력하세요: ')
Search_Num = int(input('검색할 url 개수를 입력하세요: '))
import pandas as pd
import time
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

# Selenium 초기 설정
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# 네이버 뉴스 페이지 열기
driver.get('https://www.naver.com/')
driver.find_element(By.ID, 'query').send_keys(Keyword + '\n')
driver.find_element(By.LINK_TEXT, '뉴스').click()

# 결과 저장 리스트 초기화
sn2 = []
title2 = []
url2 = []
no = 1

print("데이터 수집을 시작합니다...")

# 스크롤 반복
while len(title2) < ArticleNum:
    # 현재 페이지 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('div > a.news_tit')

    # 기사 수집
    for article in articles:
        if no > ArticleNum:
            break
        try:
            title = article.text
            url = article['href']
        except:
            continue

        # 데이터 저장
        sn2.append(no)
        title2.append(title)
        url2.append(url)

        with open(ft_name, 'a', encoding='utf-8') as f:
            f.write(f"1. 연번: {no}\n2. 기사 제목: {title}\n3. 링크: {url}\n\n")

        print(f"1. 연번: {no}\n2. 기사 제목: {title}\n3. 링크: {url}\n")
        no += 1

        # 다음 페이지로 이동
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="다음 페이지"]')
            next_button.click()
            time.sleep(2)  # 페이지 로드 대기
        except Exception as e:
            print("다음 페이지가 없습니다.")
            break

    print("데이터 수집이 완료되었습니다!")

# Pandas DataFrame 저장
df = pd.DataFrame({'연번': sn2, '기사 제목': title2, '링크': url2})
df.to_excel(fx_name, index=False, sheet_name='뉴스 기사')

driver.quit()
