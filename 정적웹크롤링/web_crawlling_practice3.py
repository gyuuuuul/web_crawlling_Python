
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

# 6. 'soup' 결과 출력 및 검색결과 html 출력. prettify()가 꼭 필요함. soup라는 객체를 string으로 변환하는 함수임.
print(soup.prettify())

with open('%s.html' %query, 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
