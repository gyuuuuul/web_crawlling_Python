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

# Selenium 초기 설정
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# 기사 제목 저장 리스트 및 번호 초기화
search_result = []
no = 1

try:
    # 구글 페이지 열기
    driver.get("https://www.google.com/")

    # 검색창에 키워드 입력 후 실행
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # 페이지 탐색 시작
    while no <= Search_Num:
        # 현재 페이지 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 모든 h3 태그 선택 (구글 검색 결과 제목)
        titles = soup.select('h3')  # 구글 검색 결과에서 h3 태그 선택

        # 데이터 수집
        for title in titles:
            if no > Search_Num:
                break
            try:
                # h3 태그의 부모 a 태그에서 URL 추출
                parent_a = title.find_parent('a')
                if parent_a:
                    title_text = title.text.strip()
                    url = parent_a['href']
                else:
                    continue
            except Exception as e:
                print(f"오류 발생: {e}")
                continue

            # 중복 확인 후 추가
            if url in [item['url'] for item in search_result]:
                continue

            search_result.append({"title": title_text, "url": url})
            print(f"{no}. {title_text}: {url}")
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

finally:
    # 브라우저 종료
    driver.quit()

# 결과 출력
if search_result:
    print(f"총 {len(search_result)}개의 데이터를 수집했습니다.")
else:
    print("수집된 데이터가 없습니다. 검색어나 구조를 확인하세요.")
