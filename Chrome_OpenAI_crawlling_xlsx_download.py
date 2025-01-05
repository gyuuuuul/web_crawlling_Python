from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import os
import openai


# API 키 설정
openai.api_key = "-보안사항 - push 안됨"

client = openai.OpenAI(api_key=openai.api_key)

# Desktop 경로 설정
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
print(desktop)

# 키워드 및 크롤링 설정
Keyword = input('1. 수집 검색어는 무엇입니까?: ')
ArticleNum = int(input('2. 몇 건을 수집하시겠습니까?: '))
user_query = input("3. 찾고 싶은 내용이나 질문을 입력하세요: ")

# 저장 파일 이름 및 경로 설정
txt_name = os.path.join(desktop, input('3.결과를 저장할 txt형식의 파일명을 쓰세요(예: 파일명.txt): '))
excel_name = os.path.join(desktop, input('4.결과를 저장할 xlsx형식의 파일명을 쓰세요(예: 파일명.xlsx): '))

# 기존 TXT 파일 초기화
with open(txt_name, 'w', encoding='utf-8') as f:
    f.write("")

# Selenium 초기 설정
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
#options.add_argument('--headless')  # 브라우저 창 숨김, 브라우저를 보면서 사용하고 싶다면 삭제하고 사용
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
openai_responses = [] # OpenAI 응답 저장 리스트

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

    tabs = []  # 현재 페이지의 탭 핸들 저장

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

            # 새 탭에서 기사 URL 열기
            driver.execute_script("window.open(arguments[0]);", url)
            tabs.append(driver.window_handles[-1])  # 열린 탭의 핸들을 저장

            # 데이터 저장
            sn2.append(current_index)
            title2.append(title)
            url2.append(url)
            site_name2.append(site_name)
            site_path2.append(site_path)
            snippet2.append(snippet)

            current_index += 1  # 연번 증가

        except Exception as e:
            print(f"URL 열기 오류: {e}")

    # 각 탭에서 본문 추출
    for i, tab in enumerate(tabs):
        driver.switch_to.window(tab)
        try:
            # 페이지 로드 대기
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            # 기사 본문 가져오기
            article_html = driver.page_source
            article_soup = BeautifulSoup(article_html, 'lxml')
            article_body_tag = article_soup.body
            article_content = article_body_tag.get_text(strip=True) if article_body_tag else "본문 없음"
            article_content2.append(article_content)

            # OpenAI API 호출
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"문서 제목: {title2[-len(tabs) + i]}\n\n 문서 본문: {article_content}\n\n 위 문서에서 질문: {user_query}의 알맞는 것을 찾아주고 질문 문서가 얼마나 유사한지 %로 표현해."}
                    ]
                )
                gpt_response = response.choices[0].message.content  # 올바른 속성 접근
            except Exception as e:
                gpt_response = f"OpenAI API 호출 중 오류 발생: {e}"

            openai_responses.append(gpt_response)

            # TXT 파일 저장
            with open(txt_name, 'a', encoding='utf-8') as f:
                f.write(f"1. 연번: {sn2[len(title2) - len(tabs) + i]}\n")
                f.write(f"2. 사이트 이름: {site_name2[len(title2) - len(tabs) + i]}\n")
                f.write(f"3. 사이트 경로: {site_path2[len(title2) - len(tabs) + i]}\n")
                f.write(f"4. 기사 제목: {title2[len(title2) - len(tabs) + i]}\n")
                f.write(f"5. 요약: {snippet2[len(title2) - len(tabs) + i]}\n")
                f.write(f"6. 링크: {url2[len(title2) - len(tabs) + i]}\n")
                f.write(f"7. OpenAI 응답:\n{gpt_response}\n\n")
                
                print(f"1. 연번: {sn2[len(title2) - len(tabs) + i]}\n2. 사이트 이름: {site_name2[len(title2) - len(tabs) + i]}\n3. 사이트 경로: {site_path2[len(title2) - len(tabs) + i]}\n4. 기사 제목: {title2[len(title2) - len(tabs) + i]}\n5. 요약: {snippet2[len(title2) - len(tabs) + i]}\n6. 링크: {url2[len(title2) - len(tabs) + i]}\n7. OpenAI 응답:\n{gpt_response}\n")

        except Exception as e:
            print(f"본문 추출 오류: {e}")
            article_content2.append("본문 없음")
            openai_responses.append("OpenAI 응답 없음")

        finally:
            driver.close()

    driver.switch_to.window(driver.window_handles[0])  # 원래 탭으로 돌아오기
    tabs.clear()  # 열린 탭 리스트 초기화

    # 다음 페이지 버튼 클릭
    try:
        next_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.ID, "pnnext"))
        )
        next_button.click()
    except Exception as e:
        print(f"다음 페이지로 넘어가는 중 오류 발생: {e}")
        break

print("데이터 수집이 완료되었습니다!")

# DataFrame 생성 전 빈 리스트 채우기
max_length = max(
    len(sn2), len(title2), len(url2), len(site_name2), len(site_path2), len(snippet2), len(openai_responses)
)

sn2 += [None] * (max_length - len(sn2))
title2 += ["제목 없음"] * (max_length - len(title2))
url2 += ["URL 없음"] * (max_length - len(url2))
site_name2 += ["사이트 이름 없음"] * (max_length - len(site_name2))
site_path2 += ["사이트 경로 없음"] * (max_length - len(site_path2))
snippet2 += ["요약 없음"] * (max_length - len(snippet2))
openai_responses += ["OpenAI 응답 없음"] * (max_length - len(openai_responses))

# Pandas DataFrame 저장
df = pd.DataFrame({
    '연번': sn2,
    '사이트 이름': site_name2,
    '사이트 경로': site_path2,
    '기사 제목': title2,
    '요약': snippet2,
    '링크': url2,
    'OpenAI 응답' : openai_responses # OpenaAI 응답 추가
})
df.to_excel(excel_name, index=False, sheet_name='뉴스 기사')

# 드라이버 종료
driver.quit()
