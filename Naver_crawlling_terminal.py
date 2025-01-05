from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup

# 검색할 키워드 입력

query = input('검색할 키워드를 입력하세요: ')
ArticleNum = int(input('검색할 기사 개수를 입력하세요: '))

# Selenium 초기 설정
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5) 

# 기사 제목 저장 리스트 및 번호 초기화
title2 = []
no = 1

try:
    # 크롬 드라이버에 원하는 url 주소 넣고 실행
    url = 'https://www.naver.com/'
    driver.get(url)

    # 검색어 창을 기다림 (최대 10초 대기)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'query'))
    )

    # 검색어 입력 및 엔터
    # 'send_keys'는 Selenium의 입력 동작 메서드, 텍스트 입력 필드(input)이나 기타 입력 가능한 요소에 키 입력(텍스트, 키보드 이벤트)을 시뮬레이션하는 데 사용

    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    news_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[role='tab'][href*='ssc=tab.news.all']"))
    )
    news_tab.click()
    
    news_titles = driver.find_elements(By.CLASS_NAME, "news_tit")
    
    # 스크롤 반복
    last_height = driver.execute_script("return document.body.scrollHeight")
    while no < ArticleNum:
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
            title2.append(title)
            print(f"{no}. {title}: {url}")
            no += 1

        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 새로운 콘텐츠 로드 확인
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    print("데이터 수집이 완료되었습니다!")
finally:
    # 브라우저 종료
    driver.quit()