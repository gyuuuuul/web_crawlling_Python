from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import os
import traceback  # 추가: 디버깅을 위한 전체 오류 출력


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
site_path2 = []
snippet2 = []
no = 1

print("데이터 수집을 시작합니다...")

# 스크롤 반복
try:
    while len(title2) < ArticleNum:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.tF2Cxc")))

        # 현재 페이지 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.select('div.tF2Cxc')  # 구글 검색 결과 블록

        print(f"검색 결과 블록 수: {len(articles)}")  # 블록 수 확인

        page_collected = 0  # 현재 페이지에서 수집한 데이터 수

        # 기사 수집
        for article in articles:
            if len(title2) >= ArticleNum:
                break
            try:
                # 제목 추출
                title = None
                title_tag = article.select_one('h3') or article.select_one('a[aria-label]') or article.select_one('a')
                if title_tag:
                    title = title_tag.text.strip()
                if not title:
                    print("제목을 찾을 수 없습니다. 현재 블록을 건너뜁니다.")
                    continue

                # URL 추출
                url_tag = article.select_one('a')
                if not url_tag:
                    print("URL을 찾을 수 없습니다. 현재 블록을 건너뜁니다.")
                    continue
                url = url_tag['href']

                # 사이트 경로 추출
                site_path_tag = article.select_one('cite')
                site_path = site_path_tag.text.strip() if site_path_tag else "사이트 경로 없음"

                # 요약 추출
                snippet_tag = article.select_one('div.VwiC3b')
                snippet = snippet_tag.text.strip() if snippet_tag else "요약 없음"

                # 사이트 이름 추출 (VuuXrf 클래스 사용)
                site_name_tag = article.select_one('span.VuuXrf')
                site_name = site_name_tag.text.strip() if site_name_tag else "사이트 이름 없음"

                # 데이터 저장
                sn2.append(len(title2) + 1)
                title2.append(title)
                url2.append(url)
                site_name2.append(site_name)
                site_path2.append(site_path)
                snippet2.append(snippet)

                # TXT 저장 (배너 링크 제거)
                with open(txt_name, 'a', encoding='utf-8') as f:
                    f.write(f"1. 연번: {len(title2)}\n")
                    f.write(f"2. 사이트 이름: {site_name}\n")
                    f.write(f"3. 사이트 경로: {site_path}\n")
                    f.write(f"4. 기사 제목: {title}\n")
                    f.write(f"5. 요약: {snippet}\n")
                    f.write(f"6. 링크: {url}\n\n")

                print(f"1. 연번: {len(title2)}\n2. 사이트 이름: {site_name}\n3. 사이트 경로: {site_path}\n4. 기사 제목: {title}\n5. 요약: {snippet}\n6. 링크: {url}\n")
            except Exception as e:
                print(f"오류 발생: {e}")
                continue

        # 다음 페이지 버튼 클릭
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(1)  # 페이지 로드 대기
        except:
            print("더 이상 페이지가 없습니다.")
            break
except Exception as e:
    print("전체 실행 중 오류 발생:", e)
    print(traceback.format_exc())  # 전체 오류 추적 출력
finally:
    # DataFrame 생성 전 빈 리스트 채우기
    max_length = max(
        len(sn2), len(title2), len(url2), len(site_name2), len(site_path2), len(snippet2)
        )

    sn2 += [None] * (max_length - len(sn2))
    title2 += ["제목 없음"] * (max_length - len(title2))
    url2 += ["URL 없음"] * (max_length - len(url2))
    site_name2 += ["사이트 이름 없음"] * (max_length - len(site_name2))
    site_path2 += ["사이트 경로 없음"] * (max_length - len(site_path2))
    snippet2 += ["요약 없음"] * (max_length - len(snippet2))

    # Pandas DataFrame 저장
    df = pd.DataFrame({
        '연번': sn2,
        '사이트 이름': site_name2,
        '사이트 경로': site_path2,
        '기사 제목': title2,
        '요약': snippet2,
        '링크': url2
    })
    df.to_excel(excel_name, index=False, sheet_name='뉴스 기사')

    # 드라이버 종료
    driver.quit()

    print("데이터 수집이 완료되었습니다!")

