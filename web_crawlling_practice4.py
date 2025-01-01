# requests와 beautifulsoup를 이용, 추출 방법
# 크롬 개발자도구에서 커서 모양의 아이콘을 클릭 -> 추출을 원하는 부분을 클릭 -> 해당 부분의 HTML 태그 및 class (ex. a와 href)를 분석하여 select( ) 함수로 추출
# 네이버 뉴스에서 태그 및 클래스는: "a.news_tit" 임.


# 1. improt로 패키지 불러오기

import requests
from bs4 import BeautifulSoup as bs

# 2. naver에 검색할 키워드 입력

query = input('검색할 키워드를 입력하세요: ')


# 3. 네이버 뉴스 검색 결과의 url은 마지막 query(키워드)만 변함. 즉, 입력한 query, 즉 키워드로 네이버 뉴스 검색을 하라는 것. 이를 저장

url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+'%s'%query

# 4. requests 패키지를 이용해 'url'(네이버 뉴스 검색 결과)의 html 문서 가져오기

response = requests.get(url)
html_text = response.text

# 5. beautifulsoup 패키지로 파싱(parsing) 후, 'soup' 변수에 저장

soup = bs(response.text, 'html.parser')

# 6.뉴스 제목 텍스트 추출

news_titles = soup.select("a.news_tit")

for i in news_titles:
    title = i.get_text()
    print(title)