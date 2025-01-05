from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 검색할 키워드 입력

query = input('검색할 키워드를 입력하세요: ')


# 크롬드라이버 실행
driver = webdriver.Chrome()

try:
    # 크롬 드라이버에 url 주소 넣고 실행
    driver.get('https://www.google.co.kr/')

    # 검색어 창을 기다림 (최대 10초 대기)
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )

    # 검색어 입력 및 엔터
    # 'send_keys'는 Selenium의 입력 동작 메서드, 텍스트 입력 필드(input)이나 기타 입력 가능한 요소에 키 입력(텍스트, 키보드 이벤트)을 시뮬레이션하는 데 사용

    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # 검색 결과가 로드될 때까지 대기 (최대 10초)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'search'))
    )

    print("검색 완료!")
finally:
    # 브라우저 종료
    driver.quit()

# 혹은 # 브라우저를 닫지 않도록 `finally` 블록 제거
# except Exception as e:
#    print(f"예외 발생: {e}")