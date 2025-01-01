# selenium 패키지 및 크롬 드라이버

# selenium: 아래의 두 가지 모듈들 import 해주어야 함.

# selenium의 webdriver를 사용하기 위한 import
# webdriver는 selenium의 클래스. 당연히 크롬의 HTML 화면에는 안나옴.

from selenium import webdriver

# selenium으로 key를 조작하기 위한 import

from selenium.webdriver.common.keys import Keys

# By는 Selenium의 "로케이터(locator)" 도구. 

from selenium.webdriver.common.by import By


# 로케이터: Selenium이 HTML 문서에서 특정 요소를 찾기 위해 사용하는 방법(전략). 다음의 탐색 방법이 있음.

속성	설명	예시
By.ID	요소의 id 속성을 기준으로 찾음	driver.find_element(By.ID, "search_box")
By.NAME	요소의 name 속성을 기준으로 찾음	driver.find_element(By.NAME, "q")
By.CLASS_NAME	요소의 class 속성을 기준으로 찾음	driver.find_element(By.CLASS_NAME, "btn-primary")
By.TAG_NAME	HTML 태그 이름을 기준으로 찾음	driver.find_element(By.TAG_NAME, "input")
By.LINK_TEXT	요소의 링크 텍스트(전체)를 기준으로 찾음	driver.find_element(By.LINK_TEXT, "클릭하세요")
By.PARTIAL_LINK_TEXT	요소의 링크 텍스트(부분)를 기준으로 찾음	driver.find_element(By.PARTIAL_LINK_TEXT, "클릭")
By.CSS_SELECTOR	CSS 선택자를 기준으로 찾음	driver.find_element(By.CSS_SELECTOR, ".nav > a")
By.XPATH	XPath 표현식을 기준으로 찾음	driver.find_element(By.XPATH, "//div[@id='main']")

# 이 중에서 By.NAME, By.ID, By.XPATH를 가장 많이 사용.
# id는 고유함. 만약, 구글에서 검색이 되었다면, id="search" 가 나오게 되어있음. 무조건 1개
# XPATH의 경우: html 코드 위에서 '우클릭' -> 'Copy Xpath' -> 클립보드에 xpath가 저장 -> 위와 같이 삽입.


# WebDriverWait는 selenium에서 제공하는 대기(Wait)클래스

from selenium.webdriver.support.ui import WebDriverWait

# Selenium의 expected_conditions 모듈(as EC로 표기)을 사용해 조건을 정의
from selenium.webdriver.support import expected_conditions as EC


# 추가적으로 페이지 로딩을 기다리는데에 사용할 time 모듈도 import 해줍니다. 이 모듈은 파이썬 내장 라이브러리에 포함되어 있어 별도 설치는 필요 없습니다.
# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time



# 크롬 드라이버를 이용해서 크롬을 실행하기
# Chrome Driver: 컴퓨터가 크롬 웹 브라우저를 다룰 수 있도록 해주는 프로그램. 구글에서 제공 
# 코드를 실행 시키시면 자동으로 다운로드 되니 별도 설치가 필요 없음. 

# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver

# 크롬드라이버 실행
driver = webdriver.Chrome() 

#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://www.google.co.kr/')

# time함수: 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)

# Keys.enter Keys.Return 은 엔터와 같은 역할 