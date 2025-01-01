# 이미지 추출. 이미지 주소 src를 갖고 있는 html을 이용

# requests와 beautifulsoup를 이용, 추출 방법
# 크롬 개발자도구에서 커서 모양의 아이콘을 클릭 -> 추출을 원하는 부분을 클릭 -> 해당 부분의 HTML 태그 및 속성을 (ex. a와 href)를 분석하여 select( ) 함수로 추출
# 네이버 뉴스에서 태그 및 속성(attrs)는: "a.news_tit" 임.

# src주소를 news_thumnail 변수에 저장 -> 이미지 다운로드를 위해서 해당 주소들을 리스트(link_thumnail)에 append 함수 이용해 하나씩 담기.
# 사진을 다운로드 받아서 내 PC에 저장하기 위해서는 저장할 폴더를 만들고, src 주소를 이용해 다운로드 
# 폴더 생성에는 os 모듈과 urllib.request 패키지의 urlretrieve 함수가 필요. 모두 다 파이썬 내장 라이브러리이므로 설치 필요X. import 하면 됨.

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

# 6. 뉴스 썸네일 이미지 추출

news_content_div = soup.select(".news_contents")

news_thumbnail = [thumbnail.select_one(".thumb") for thumbnail in news_content_div]

link_thumbnail = []

for img in news_thumbnail:
    if img is  not  None  and  'data-lazysrc'  in img.attrs:
        link_thumbnail.append(img.attrs['data-lazysrc'])

# 이미지 저장할 폴더 생성
import os

# path_folder의 경로로 저장할 폴더의 경로를 적어줄 것 (ex.img_download)
path_folder = '/Users/byeonseongjun/Desktop/img_download/'

if not os.path.isdir(path_folder):
    os.mkdir(path_folder)

# 이미지 다운로드
from urllib.request import urlretrieve

i = 0

for link in link_thumbnail:          
    i += 1
    urlretrieve(link, path_folder + f'{i}.jpg')