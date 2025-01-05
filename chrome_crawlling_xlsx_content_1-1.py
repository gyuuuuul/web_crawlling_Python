from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import os
from readability import Document



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
#options.add_argument('--headless')  # 브라우저 창 숨김
#options.add_argument('--disable-dev-shm-usage')
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
site_path2 = []
snippet2 = []
article_content2 = []  # 전체 본문 저장 리스트

# 연번 초기값
current_index = 1  # 전체 연번을 관리하는 변수

print("데이터 수집을 시작합니다...")

# 스크롤 반복
while len(title2) < ArticleNum:
    WebDriverWait(driver, 120).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.tF2Cxc"))
    )

    # 현재 페이지 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.select('div.tF2Cxc')  # 구글 검색 결과 블록

    print(f"검색 결과 블록 수: {len(articles)}")  # 블록 수 확인

    for article in articles[:min(len(articles), ArticleNum - len(title2))]:
        try:
            # 제목 및 URL 추출
            title_tag = article.select_one('h3')
            title = title_tag.text.strip() if title_tag else "제목 없음"

            url_tag = article.select_one('a')
            url = url_tag['href'] if url_tag else None

            site_path_tag = article.select_one('cite')
            site_path = site_path_tag.text.strip() if site_path_tag else "사이트 경로 없음"

            snippet_tag = article.select_one('div.VwiC3b')
            snippet = snippet_tag.text.strip() if snippet_tag else "요약 없음"

            site_name_tag = article.select_one('span.VuuXrf')
            site_name = site_name_tag.text.strip() if site_name_tag else "사이트 이름 없음"

            # 기사 본문 추출
            driver.execute_script("window.open(arguments[0]);", url)
            driver.switch_to.window(driver.window_handles[-1])

            # 페이지 로드 대기
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            doc = Document(driver.page_source)
            article_html = doc.summary()
            article_content = BeautifulSoup(article_html, 'lxml').get_text(strip=True) if article_html else "본문 없음"
            article_content2.append(article_content)

            # TXT 저장
            with open(txt_name, 'a', encoding='utf-8') as f:
                f.write(f"1. 연번: {current_index}\n")
                f.write(f"2. 사이트 이름: {site_name}\n")
                f.write(f"3. 사이트 경로: {site_path}\n")
                f.write(f"4. 기사 제목: {title}\n")
                f.write(f"5. 요약: {snippet}\n")
                f.write(f"6. 링크: {url}\n")
                f.write(f"7. 본문:\n{article_content}\n\n")

            print(f"1. 연번: {current_index}\n2. 사이트 이름: {site_name}\n3. 사이트 경로: {site_path}\n4. 기사 제목: {title}\n5. 요약: {snippet}\n6. 링크: {url}\n7. 본문:\n{article_content}\n")

            # 데이터 저장
            sn2.append(current_index)
            title2.append(title)
            url2.append(url)
            site_name2.append(site_name)
            site_path2.append(site_path)
            snippet2.append(snippet)

            # 연번 증가
            current_index += 1

            driver.close()
            driver.switch_to.window(driver.window_handles[0])  # 원래 탭으로 돌아오기

        except Exception as e:
            print(f"본문 추출 오류: {e}")

            # 누락된 데이터를 위한 빈 값 추가
            sn2.append(current_index)
            title2.append("제목 없음")
            url2.append("URL 없음")
            site_name2.append("사이트 이름 없음")
            site_path2.append("사이트 경로 없음")
            snippet2.append("요약 없음")
            article_content2.append("본문 없음")

            # 연번 증가
            current_index += 1

            driver.close()
            driver.switch_to.window(driver.window_handles[0])  # 원래 탭으로 돌아오기

    # 다음 페이지 버튼 클릭
    try:
        next_button = WebDriverWait(driver, 120).until(  # 대기
            EC.element_to_be_clickable((By.ID, "pnnext"))
        )
        next_button.click()
    except:
        print("더 이상 페이지가 없습니다.")
        break

print("데이터 수집이 완료되었습니다!")

# Pandas DataFrame 저장
df = pd.DataFrame({
    '연번': sn2,
    '사이트 이름': site_name2,
    '사이트 경로': site_path2,
    '기사 제목': title2,
    '요약': snippet2,
    '링크': url2,
    '본문': article_content2  # 본문 추가
})
df.to_excel(excel_name, index=False, sheet_name='뉴스 기사')

# 드라이버 종료
driver.quit()
